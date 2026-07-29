import boto3
import os
from botocore.exceptions import ClientError


def criar_bucket_e_estrutura(bucket_name: str, region: str = "us-east-1"):
    s3 = boto3.client("s3", region_name=region)

    # Criar bucket se não existir
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' já existe.")
    except ClientError:
        print(f"Criando bucket '{bucket_name}'...")
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )

    print("Criando diretórios obrigatórios...")

    # Lista de diretórios
    paths = [
        "raw/clientes/",
        "raw/enderecos/",
        "stage/clientes/",
        "stage/enderecos/",
        "analytics/clientes/"
    ]

    for path in paths:
        s3.put_object(Bucket=bucket_name, Key=f"{path}")
        print(f"✓ Criado: s3://{bucket_name}/{path}")

    print("Estrutura de S3 criada com sucesso!")


if __name__ == "__main__":
    BUCKET = os.getenv("S3_BUCKET_NAME", "meu-bucket-desafio")
    criar_bucket_e_estrutura(BUCKET)
