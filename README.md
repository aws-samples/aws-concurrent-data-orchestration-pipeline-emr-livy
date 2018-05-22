# AWS Concurrent Data Orchestration Pipeline EMR Livy
This code demonstrates the architecture featured on the AWS Big Data blog (https://aws.amazon.com/blogs/big-data/ ) which creates a concurrent data pipeline by using Amazon EMR and Apache Livy. This pipeline is orchestrated by Apache Airflow.

### Description of the project folders
##### cloudformation
This folder contains the cloudformation template that spins up the Airflow infrastructure.

##### dags/airflowlib
This folder contains reusable code for Amazon EMR and Apache Livy.

##### dags/transform
This folder contains sample transformation scala code which transforms the movielens data files from csv to parquet.

#####  dags/movielens_dag.py
This script contains the code for the DAG definition. It basically defines the Airflow pipeline.

### License
This library is licensed under the Apache 2.0 License.
