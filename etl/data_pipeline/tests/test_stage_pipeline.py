import os
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_pipeline.scripts.pipeline_stage import executar_pipeline_stage
from data_pipeline.configs.spark_session import get_spark_session

BASE_PATH = "./data_pipeline/data_lake"


def write_parquet_local(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path, compression="snappy")


def clear_data_lake():
    if os.path.exists(BASE_PATH):
        shutil.rmtree(BASE_PATH)


def test_stage_pipeline_end_to_end():

    clear_data_lake()

    df_clientes = pd.DataFrame([
        {"id_cliente": 1, "nome": "Lucas", "data_processamento": "2024-01-01"},
        {"id_cliente": 1, "nome": "Lucas v2", "data_processamento": "2024-01-02"},
        {"id_cliente": 2, "nome": "Ana", "data_processamento": "2024-01-05"},
    ])

    df_enderecos = pd.DataFrame([
        {"id_endereco": 10, "id_cliente": 1, "cep": "01001-000", "data_processamento": "2024-01-01"},
        {"id_endereco": 10, "id_cliente": 1, "cep": "01001-111", "data_processamento": "2024-01-03"},
    ])

    write_parquet_local(df_clientes, f"{BASE_PATH}/raw/clientes/clientes.parquet")
    write_parquet_local(df_enderecos, f"{BASE_PATH}/raw/enderecos/enderecos.parquet")

    executar_pipeline_stage(base_path=BASE_PATH)

    spark = get_spark_session()

    df_cli_stage = spark.read.parquet(f"{BASE_PATH}/stage/clientes").toPandas()
    df_end_stage = spark.read.parquet(f"{BASE_PATH}/stage/enderecos").toPandas()

    row = df_cli_stage[df_cli_stage["id_cliente"] == 1].iloc[0]
    assert row["nome"] == "Lucas v2"

    assert 2 in df_cli_stage["id_cliente"].values

    row_end = df_end_stage[df_end_stage["id_endereco"] == 10].iloc[0]
    assert row_end["cep"] == "01001-111"

    assert "data_atualizacao" in df_cli_stage.columns
    assert "data_atualizacao" in df_end_stage.columns

    spark.stop()