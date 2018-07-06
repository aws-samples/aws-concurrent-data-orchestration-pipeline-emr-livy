import airflowlib.emr_lib as emr
import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 11, 01),
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    'provide_context': True
}

# Initialize the DAG
# Concurrency --> Number of tasks allowed to run concurrently
dag = DAG('transform_movielens', concurrency=3, schedule_interval=None, default_args=default_args)
region = emr.get_region()
emr.client(region_name=region)

# Creates an EMR cluster
def create_emr(**kwargs):
    cluster_id = emr.create_cluster(region_name=region, cluster_name='movielens_cluster', num_core_nodes=2)
    return cluster_id

# Waits for the EMR cluster to be ready to accept jobs
def wait_for_completion(**kwargs):
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    emr.wait_for_cluster_creation(cluster_id)

# Terminates the EMR cluster
def terminate_emr(**kwargs):
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    emr.terminate_cluster(cluster_id)

# Converts each of the movielens datafile to parquet
def transform_movies_to_parquet(**kwargs):
    # ti is the Task Instance
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    cluster_dns = emr.get_cluster_dns(cluster_id)
    headers = emr.create_spark_session(cluster_dns, 'spark')
    session_url = emr.wait_for_idle_session(cluster_dns, headers)
    statement_response = emr.submit_statement(session_url,
                                              '/root/airflow/dags/transform/movies.scala')
    emr.track_statement_progress(cluster_dns, statement_response.headers)
    emr.kill_spark_session(session_url)

def transform_tags_to_parquet(**kwargs):
    # ti is the Task Instance
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    cluster_dns = emr.get_cluster_dns(cluster_id)
    headers = emr.create_spark_session(cluster_dns, 'spark')
    session_url = emr.wait_for_idle_session(cluster_dns, headers)
    statement_response = emr.submit_statement(session_url,
                                              '/root/airflow/dags/transform/tags.scala')
    emr.track_statement_progress(cluster_dns, statement_response.headers)
    emr.kill_spark_session(session_url)

def transform_ratings_to_parquet(**kwargs):
    # ti is the Task Instance
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    cluster_dns = emr.get_cluster_dns(cluster_id)
    headers = emr.create_spark_session(cluster_dns, 'spark')
    session_url = emr.wait_for_idle_session(cluster_dns, headers)
    statement_response = emr.submit_statement(session_url,
                                              '/root/airflow/dags/transform/ratings.scala')
    emr.track_statement_progress(cluster_dns, statement_response.headers)
    emr.kill_spark_session(session_url)

def transform_links_to_parquet(**kwargs):
    # ti is the Task Instance
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    cluster_dns = emr.get_cluster_dns(cluster_id)
    headers = emr.create_spark_session(cluster_dns, 'spark')
    session_url = emr.wait_for_idle_session(cluster_dns, headers)
    statement_response = emr.submit_statement(session_url,
                                              '/root/airflow/dags/transform/links.scala')
    emr.track_statement_progress(cluster_dns, statement_response.headers)
    emr.kill_spark_session(session_url)

def transform_genome_scores_to_parquet(**kwargs):
    # ti is the Task Instance
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    cluster_dns = emr.get_cluster_dns(cluster_id)
    headers = emr.create_spark_session(cluster_dns, 'spark')
    session_url = emr.wait_for_idle_session(cluster_dns, headers)
    statement_response = emr.submit_statement(session_url,
                                              '/root/airflow/dags/transform/genome_scores.scala')
    emr.track_statement_progress(cluster_dns, statement_response.headers)
    emr.kill_spark_session(session_url)

def transform_genome_tags_to_parquet(**kwargs):
    # ti is the Task Instance
    ti = kwargs['ti']
    cluster_id = ti.xcom_pull(task_ids='create_cluster')
    cluster_dns = emr.get_cluster_dns(cluster_id)
    headers = emr.create_spark_session(cluster_dns, 'spark')
    session_url = emr.wait_for_idle_session(cluster_dns, headers)
    statement_response = emr.submit_statement(session_url,
                                              '/root/airflow/dags/transform/genome_tags.scala')
    emr.track_statement_progress(cluster_dns, statement_response.headers)
    emr.kill_spark_session(session_url)

# Define the individual tasks using Python Operators
create_cluster = PythonOperator(
    task_id='create_cluster',
    python_callable=create_emr,
    dag=dag)

wait_for_cluster_completion = PythonOperator(
    task_id='wait_for_cluster_completion',
    python_callable=wait_for_completion,
    dag=dag)

transform_movies = PythonOperator(
    task_id='transform_movies',
    python_callable=transform_movies_to_parquet,
    dag=dag)

transform_ratings = PythonOperator(
    task_id='transform_ratings',
    python_callable=transform_ratings_to_parquet,
    dag=dag)

transform_tags = PythonOperator(
    task_id='transform_tags',
    python_callable=transform_tags_to_parquet,
    dag=dag)

transform_links = PythonOperator(
    task_id='transform_links',
    python_callable=transform_links_to_parquet,
    dag=dag)

transform_genome_scores = PythonOperator(
    task_id='transform_genome_scores',
    python_callable=transform_genome_scores_to_parquet,
    dag=dag)

transform_genome_tags = PythonOperator(
    task_id='transform_genome_tags',
    python_callable=transform_genome_tags_to_parquet,
    dag=dag)


terminate_cluster = PythonOperator(
    task_id='terminate_cluster',
    python_callable=terminate_emr,
    trigger_rule='all_done',
    dag=dag)

# construct the DAG by setting the dependencies
create_cluster >> wait_for_cluster_completion
wait_for_cluster_completion >> transform_movies >> terminate_cluster
wait_for_cluster_completion >> transform_ratings >> terminate_cluster
wait_for_cluster_completion >> transform_links >> terminate_cluster
wait_for_cluster_completion >> transform_tags >> terminate_cluster
wait_for_cluster_completion >> transform_genome_scores >> terminate_cluster
wait_for_cluster_completion >> transform_genome_tags >> terminate_cluster
