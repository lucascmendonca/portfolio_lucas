import os
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from data_pipeline.scripts.pipeline_analytics import executar_pipeline_analytics
from data_pipeline.configs.spark_session import get_spark_session

BASE_PATH = "./data_pipeline/data_lake"


def write_parquet(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)


def limpar():
    if os.path.exists(BASE_PATH):
        shutil.rmtree(BASE_PATH)


def test_pipeline_analytics():

    limpar()

    df_clientes = pd.DataFrame([
        {"id_cliente": 1, "nome": "Lucas", "status": "ativo", "data_nascimento": "1990-10-10"},
        {"id_cliente": 2, "nome": "Ana", "status": "inativo", "data_nascimento": "1988-01-01"},
    ])

    df_enderecos = pd.DataFrame([
        {"id_endereco": 10, "id_cliente": 1, "cep": "01001-000"},
        {"id_endereco": 11, "id_cliente": 1, "cep": "01001-200"},
    ])

    write_parquet(df_clientes, f"{BASE_PATH}/stage/clientes/clientes.parquet")
    write_parquet(df_enderecos, f"{BASE_PATH}/stage/enderecos/enderecos.parquet")

    executar_pipeline_analytics(base_path=BASE_PATH)

    spark = get_spark_session()

    df_final = spark.read.parquet(f"{BASE_PATH}/analytics/clientes").toPandas()

    assert 1 in df_final["id_cliente"].values
    assert 2 not in df_final["id_cliente"].values

    assert len(df_final[df_final["id_cliente"] == 1]["id_endereco"]) == 2

    assert "idade" in df_final.columns

    spark.stop()
