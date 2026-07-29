import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
from datetime import date


def write_parquet_local(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path, compression="snappy")
    print(f"[LOCAL] Arquivo escrito: {path}")


def write_parquet_s3(df: pd.DataFrame, bucket: str, key: str):
    table = pa.Table.from_pandas(df)
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer, compression="snappy")

    boto3.client("s3").put_object(
        Bucket=bucket,
        Key=key,
        Body=buffer.getvalue().to_pybytes()
    )

    print(f"[AWS S3] Arquivo escrito em s3://{bucket}/{key}")


def salvar_raw(
    df: pd.DataFrame,
    nome_dataset: str,
    valido: bool,
    environment: str = "local",
    bucket: str = "",
    output_dir: str = "./local_output"
):

    data_particao = date.today().isoformat()

    # Caminhos dentro da estrutura RAW
    if valido:
        caminho_relativo = f"raw/{nome_dataset}/data_processamento={data_particao}/raw_{nome_dataset}.parquet"
    else:
        caminho_relativo = f"raw/erros/{nome_dataset}/{nome_dataset}_erro.parquet"

 
    # MODO LOCAL
 
    if environment == "local":
        full_path = os.path.join(output_dir, caminho_relativo)
        write_parquet_local(df, full_path)

 
    # MODO AWS
 
    elif environment == "aws":
        if not bucket:
            raise ValueError("Bucket S3 não informado.")
        write_parquet_s3(df, bucket, caminho_relativo)

    else:
        raise ValueError("Environment deve ser 'local' ou 'aws'.")