import os
import pandas as pd
import pytest
from unittest.mock import patch
from moto import mock_aws
import boto3

from scripts.pipeline_raw import executar_pipeline_raw



# Teste LOCAL

@patch("data_pipeline.scripts.pipeline_raw.extracao_excel_github")
@patch("data_pipeline.scripts.pipeline_raw.salvar_raw")
def test_pipeline_raw_local(mock_salvar_raw, mock_extract):

    # Simulação correta do retorno do Excel
    mock_extract.return_value = {
        "clientes": pd.DataFrame([
            {
                "id_cliente": 1,
                "nome": "Lucas",
                "cpf": "11144477735",
                "email": "teste@example.com",
                "data_nascimento": "1990-10-10",
                "status": "ativo",
            }
        ]),
        "enderecos": pd.DataFrame([
            {
                "id_cliente": 1,
                "cep": "01001-000",
                "cidade": "São Paulo",
                "estado": "SP"
            }
        ])
    }

    os.environ["ENVIRONMENT"] = "local"

    executar_pipeline_raw()

    # Verificar que o writer foi chamado
    assert mock_salvar_raw.called
    assert mock_salvar_raw.call_count >= 2  # válidos + inválidos ou só válidos



# Teste S3 usando Moto

@mock_aws
@patch("data_pipeline.scripts.pipeline_raw.extracao_excel_github")
def test_pipeline_raw_s3(mock_extract):

    mock_extract.return_value = {
        "clientes": pd.DataFrame([
            {
                "id_cliente": 1,
                "nome": "Lucas",
                "cpf": "11144477735",
                "email": "teste@example.com",
                "data_nascimento": "1990-10-10",
                "status": "ativo",
            }
        ]),
        "enderecos": pd.DataFrame([
            {
                "id_cliente": 1,
                "cep": "01001-000",
                "cidade": "São Paulo",
                "estado": "SP"
            }
        ])
    }

    os.environ["ENVIRONMENT"] = "aws"
    os.environ["S3_BUCKET_NAME"] = "meu-bucket-test"

    # Criar bucket mockado
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="meu-bucket-test")

    executar_pipeline_raw()

    # Conferir se salvou dentro do bucket
    response = s3.list_objects_v2(Bucket="meu-bucket-test")

    assert "Contents" in response
    assert len(response["Contents"]) > 0
