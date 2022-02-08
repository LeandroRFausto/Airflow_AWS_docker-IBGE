# Playbook: Airflow_AWS_Docker

Desenvolve uma DAG "Pipline" que requisita dados ao MongoDB e a API do IBGE. São montadas duas estruturas que realizam upload desses dados para um banco relacional e para um bucket S3 na AWS. Para consumo no DataLake foram utilizados como serverless o AWS Glue (crawler) e AWS Athena. A ferramenta visual utilizada foi o Amazon QuickSight.

# Descrição
#### Componentes utilizados:
* **Sistema operacional: windows 11 com Ubuntu 20.04 rodando em WSL2**
* **Python**
* **Docker**
* **Airflow**
* **MongoDB**
* **Postgres**
* **Amazon_S3**
* **AWS_GLUE**
* **AWS_ATHENA**
* **Amazon_QuickSight**

# Configuração
A pasta docker-airflow-igti_desafio_final contém os requisitos de ambiente para rodar o projeto.
Necessário importar pacotes que serão utilizados no arquivo dag_IBGE.py.
Quaisquer aplicações não presentes necessárias a execução deverão ser baixadas. 

<p align="center">
<img src="https://github.com/LeandroRFausto/Airflow_AWS_docker-IBGE/AWS/Arquitetura_DAG_IBGE.pptx" alt="Image" height="300" width="600"/>
</p>

# Uso
Para iniciar a implantação, inicie o Docker:
    
    sudo service docker start

 navegue até a pasta onde se encontra o ambiente e execute:
    
    docker-compose -f docker-compose-CeleryExecutor.yml up -d --scale worker=2

O ambiente é escalável, nesta aplicação foram utilizados 2 "workers".

A configuração define o Airflow no http://localhost:8080/ .

* Para autorizar as requisições do MongoDB e AWS é necessário inserir as chaves no Airflow. Para isso, navegue até Admin/Variables e crie as chaves de ambos com as respectivas senhas.

* Execute a DAG

<p align="center">
<img src="https://github.com/LeandroRFausto/Airflow_AWS_docker-IBGE/GraphView_dag.png" alt="Image" height="300" width="600"/>
</p>

* O Graph View deverá demonstrar todos os trabalhos em verde. Quando o status for "success", abra o SGBD de sua preferência. Lá estarão disponíveis os arquivos dimensao_messoregioes_RJ.csv e pnadc20203.csv, os mesmos presentes no AWS S3. Na pasta DB_relacional deste projeto há dois arquivos de extensão .sql gerados para consulta através do SGBD.

* No Aws Glue crie um novo crawler. Ele irá identificar os esquemas e enviará as tabelas para consumo no Athena. Os arquivos de extensão .csv encontrados na pasta AWS desse projeto são oriundos da consulta. 

* O Amazon QuickSight foi utilizado para construção de Dashboards, entretanto eles também pode ser usado para insights.

<p align="center">
<img src="https://github.com/LeandroRFausto/Airflow_AWS_docker-IBGE/AWS/Dashboard_IBGE.jpg" alt="Image" height="300" width="600"/>
</p>




