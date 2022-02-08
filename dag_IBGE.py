
from airflow.decorators import dag, task
from datetime import datetime, timedelta
import pandas as pd
import requests
import json
import boto3
import os
import pymongo
from sqlalchemy import create_engine
from airflow.models import Variable 

# Captura as variáveis de ambiente cadastradas no Airflow
aws_access_key_id = Variable.get('aws_access_key_id')
aws_secret_access_key = Variable.get('aws_secret_access_key')
mongo_password = Variable.get('mongo_password')

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Define as default args
default_args = {
    'owner': 'Leandro Fausto',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
} 

# Define a DAG e suas tasks
@dag(default_args=default_args, schedule_interval='@once', catchup=False, description='Desafio final IGTI', tags=['mongo', 'python', 'Postgres'])
def igti_desafio_final_edd():
    """
    Flow que obtem dados do IBGE de uma base MongoDB, da API de microrregiões do IBGE,
    deposita no datalake no s3 e no DW em um PostgreSQL local
    """

    @task
    def extrai_mongo():
        data_path = '/usr/local/airflow/data/pnadc20203.csv'
        client = pymongo.MongoClient(f'mongodb+srv://estudante_igti:{mongo_password}@unicluster.ixhvw.mongodb.net/ibge?retryWrites=true&w=majority')
        db = client.ibge
        pnad_collec = db.pnadc20203
        df = pd.DataFrame(list(pnad_collec.find()))
        df.to_csv(data_path, index=False, encoding='utf-8', sep=';')
        return data_path

    @task
    def extrai_api():
        data_path = '/usr/local/airflow/data/dimensao_mesorregioes_rj.csv'
        url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/RJ/mesorregioes'
        response = requests.get(url)
        response_json = json.loads(response.text)
        df = pd.DataFrame(response_json)[['id', 'nome']]
        df.to_csv(data_path, index=False, encoding='utf-8', sep=';')
        return data_path

    @task
    def upload_to_s3(file_name):
        print(f"Got filename: {file_name}")
        print(f"Got object_name: {file_name[19:]}")
        s3_client.upload_file(file_name, 'igtibootcamped2021540508219347', f"raw-data/desafio_final/{file_name[19:]}")

    @task
    def write_to_postgres(csv_file_path):
        engine = create_engine('postgresql://airflow:airflow@postgres:5432/postgres')
        df = pd.read_csv(csv_file_path, sep=';')
        if csv_file_path == '/usr/local/airflow/data/pnadc20203.csv':
            df = df.loc[(df.idade >= 20) & (df.idade <=40) & (df.sexo == 'Mulher')]
        df.to_sql(csv_file_path[24:-4], engine, if_exists='replace', index=False, method='multi', chunksize=1000)

    # Orquestração
    mongo = extrai_mongo()
    api = extrai_api()

    upmongo = upload_to_s3(mongo)
    upapi = upload_to_s3(api)

    wrmongo = write_to_postgres(mongo)
    wrapi = write_to_postgres(api)

execucao = igti_desafio_final_edd()

