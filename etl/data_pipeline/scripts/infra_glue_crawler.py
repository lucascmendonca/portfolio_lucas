import boto3
import os


def criar_glue_crawler(
    crawler_name: str,
    bucket_name: str,
    role_arn: str,
    database_name: str = "clientes_db",
    region: str = "us-east-1"
):
    glue = boto3.client("glue", region_name=region)

    # Caminho no S3 apontando para a camada analytics
    s3_target_path = f"s3://{bucket_name}/analytics/clientes/"

    # Criar database se não existir
    try:
        glue.get_database(Name=database_name)
        print(f"Database '{database_name}' já existe.")
    except glue.exceptions.EntityNotFoundException:
        print(f"Criando database '{database_name}'...")
        glue.create_database(
            DatabaseInput={
                "Name": database_name,
                "Description": "Database para o desafio de engenharia de dados"
            }
        )

    # Criar o crawler
    print(f"Criando crawler '{crawler_name}'...")
    glue.create_crawler(
        Name=crawler_name,
        Role=role_arn,
        DatabaseName=database_name,
        Targets={
            "S3Targets": [
                {"Path": s3_target_path}
            ]
        },
        TablePrefix="clientes_",
        Description="Crawler que lê dados da camada analytics do desafio.",
        Schedule=None,
    )

    print("Crawler criado com sucesso!")

    # Executar o crawler
    print("Executando crawler...")
    glue.start_crawler(Name=crawler_name)
    print("Crawler iniciado.")


if __name__ == "__main__":
    BUCKET = os.getenv("S3_BUCKET_NAME", "meu-bucket-desafio")
    ROLE_ARN = os.getenv("CRAWLER_ROLE_ARN")

    criar_glue_crawler(
        crawler_name="crawler_clientes_analytics",
        bucket_name=BUCKET,
        role_arn=str(ROLE_ARN)
    )
