import os
import pandas as pd
import pyarrow.parquet as pq
from moto import mock_aws
import boto3
from datetime import date

from data_pipeline.scripts.raw_writer import salvar_raw



# TESTE: salvar RAW no S3 utilizando Moto (mock S3)

@mock_aws
def test_salvar_raw_s3_valido():
    # Criar bucket fake
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket = "meu-bucket-teste"
    s3.create_bucket(Bucket=bucket)

    # 2) DataFrame de teste
    df = pd.DataFrame({
        "id": [1, 2],
        "nome": ["Lucas", "Ana"]
    })

    # Rodar a escrita RAW no modo AWS (Moto intercepta boto3)
    salvar_raw(
        df=df,
        nome_dataset="clientes",
        valido=True,
        environment="aws",
        bucket=bucket
    )

    # Validar conteúdo do S3
    data_particao = date.today().isoformat()
    prefixo = f"raw/clientes/data_processamento={data_particao}/"

    # listar arquivos no prefixo
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefixo)
    assert "Contents" in response, "Nenhum arquivo encontrado no mock S3."

    # pegar a key do parquet
    key = response["Contents"][0]["Key"]

    # Ler o parquet diretamente do S3 (Moto)
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    parquet_bytes = s3_object["Body"].read()

    # salvar temporariamente só para ler com pyarrow
    temp_path = "temp_test.parquet"
    with open(temp_path, "wb") as f:
        f.write(parquet_bytes)

    table = pq.read_table(temp_path)
    df_lido = table.to_pandas()

    # Validar conteúdo
    assert len(df_lido) == 2
    assert df_lido.iloc[0]["nome"] == "Lucas"

    # limpar arquivo temporário
    os.remove(temp_path)



# TESTE: salvar dados inválidos no bucket utilizando Moto

@mock_aws
def test_salvar_raw_s3_invalido():
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket = "bucket-erros"
    s3.create_bucket(Bucket=bucket)

    df = pd.DataFrame({
        "id": [99],
        "erro": ["CPF inválido"]
    })

    salvar_raw(
        df=df,
        nome_dataset="clientes",
        valido=False,
        environment="aws",
        bucket=bucket
    )

    # Validar
    prefixo = "raw/erros/clientes/erro.parquet"

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefixo)
    assert "Contents" in response, "Arquivo de erro não encontrado no mock S3."

    key = response["Contents"][0]["Key"]
    obj = s3.get_object(Bucket=bucket, Key=key)
    parquet_bytes = obj["Body"].read()

    temp_path = "temp_test_error.parquet"
    with open(temp_path, "wb") as f:
        f.write(parquet_bytes)

    table = pq.read_table(temp_path)
    df_lido = table.to_pandas()

    assert df_lido.iloc[0]["erro"] == "CPF inválido"

    os.remove(temp_path)