# spark_session.py
from pyspark.sql import SparkSession
import os
import sys



def get_spark_session():
    """
    Cria uma SparkSession simples, local e totalmente compatível
    com Windows (sem Delta, sem Hadoop, sem winutils).
    """
    spark = (
        SparkSession.builder
        .appName("pipeline-local")
        .master("local")
        .getOrCreate()
    )
    return spark
