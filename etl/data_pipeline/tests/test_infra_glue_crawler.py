import boto3
from moto import mock_aws
from data_pipeline.scripts.infra_glue_crawler import criar_glue_crawler


@mock_aws
def test_criar_glue_crawler():

    region = "us-east-1"
    bucket_name = "bucket-teste"
    role_arn = "arn:aws:iam::123456789012:role/GlueTestRole"

    # Criar bucket mockado
    s3 = boto3.client("s3", region_name=region)
    s3.create_bucket(Bucket=bucket_name)

    # Executar função real
    criar_glue_crawler(
        crawler_name="crawler_teste",
        bucket_name=bucket_name,
        role_arn=role_arn,
        database_name="clientes_db",
        region=region
    )

    glue = boto3.client("glue", region_name=region)

    # SE Database criado?
    dbs = glue.get_databases()
    assert any(db["Name"] == "clientes_db" for db in dbs["DatabaseList"])

    # SE Crawler criado?
    crawler = glue.get_crawler(Name="crawler_teste")
    assert crawler["Crawler"]["Name"] == "crawler_teste"

    # SE Crawler aponta para analytics/clientes/
    targets = crawler["Crawler"]["Targets"]["S3Targets"]
    assert targets[0]["Path"] == f"s3://{bucket_name}/analytics/clientes/"