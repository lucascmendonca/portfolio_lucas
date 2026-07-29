import os
from pyspark.sql import functions as F
from data_pipeline.configs.spark_session import get_spark_session

def calcular_idade(col):
    return F.floor(F.datediff(F.current_date(), col) / 365.25)


def executar_pipeline_analytics(base_path="./data_pipeline/data_lake"):
    """
    Pipeline Analytics sem Delta Lake.
    Lê Stage Parquet, faz JOIN, cria idade e salva Parquet.
    """

    STAGE_CLIENTES = f"{base_path}/stage/clientes"
    STAGE_ENDERECOS = f"{base_path}/stage/enderecos"
    ANALYTICS_PATH = f"{base_path}/analytics/clientes"

    os.makedirs(ANALYTICS_PATH, exist_ok=True)

    spark = get_spark_session()

    print("Lendo tabelas STAGE (Parquet)...")

    clientes = spark.read.parquet(STAGE_CLIENTES)
    enderecos = spark.read.parquet(STAGE_ENDERECOS)

    print("Filtrando clientes ativos...")
    clientes_ativos = clientes.filter(F.col("status") == "ativo")

    print("LEFT JOIN com endereços...")
    df_join = clientes_ativos.alias("c").join(
        enderecos.alias("e"),
        on="id_cliente",
        how="left"
    )

    print("Calculando idade...")
    df_final = df_join.withColumn("idade", calcular_idade(F.col("data_nascimento")))

    print("Ordenando e otimizando...")
    df_final = df_final.orderBy("id_cliente").coalesce(1)

    print("Salvando Analytics em Parquet...")
    df_final.write.mode("overwrite").parquet(ANALYTICS_PATH)

    spark.stop()

    print("Pipeline Analytics finalizado.")