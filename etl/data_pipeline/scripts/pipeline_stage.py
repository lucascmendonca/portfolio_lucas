import os
from data_pipeline.configs.spark_session import get_spark_session
from data_pipeline.scripts.stage_processing import deduplicar


def executar_pipeline_stage(base_path="./data_pipeline/data_lake"):


    RAW_PATH = f"{base_path}/raw"
    STAGE_PATH = f"{base_path}/stage"

    os.makedirs(STAGE_PATH, exist_ok=True)

    spark = get_spark_session()

    print("Lendo RAW local...")

    df_clientes = spark.read.parquet(f"{RAW_PATH}/clientes")
    df_enderecos = spark.read.parquet(f"{RAW_PATH}/enderecos")

    print("Deduplicando clientes...")
    df_clientes_stage = deduplicar(df_clientes, "id_cliente", "data_processamento")

    print("Deduplicando endereços...")
    df_enderecos_stage = deduplicar(df_enderecos, "id_endereco", "data_processamento")

    print("Salvando STAGE local (Parquet)...")

    df_clientes_stage.write.mode("overwrite").parquet(f"{STAGE_PATH}/clientes")
    df_enderecos_stage.write.mode("overwrite").parquet(f"{STAGE_PATH}/enderecos")

    print("Pipeline STAGE finalizado.")

    spark.stop()
