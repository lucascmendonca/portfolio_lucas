import boto3
from moto import mock_aws
from data_pipeline.scripts.infra_s3_setup import criar_bucket_e_estrutura


@mock_aws
def test_criar_bucket_e_estrutura():

    bucket = "bucket-teste"
    region = "us-east-1"

    # Chama função que queremos testar
    criar_bucket_e_estrutura(bucket, region)

    # S3 mockado
    s3 = boto3.client("s3", region_name=region)

    # Bucket existe?
    buckets = s3.list_buckets()["Buckets"]
    assert any(b["Name"] == bucket for b in buckets)

    # Diretórios esperados?
    expected_keys = [
        "raw/clientes/",
        "raw/enderecos/",
        "stage/clientes/",
        "stage/enderecos/",
        "analytics/clientes/"
    ]

    response = s3.list_objects_v2(Bucket=bucket)

    returned_keys = [obj["Key"] for obj in response.get("Contents", [])]

    for key in expected_keys:
        assert key in returned_keys