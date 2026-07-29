import os
from dotenv import load_dotenv

load_dotenv()

# Caminho: Excel no GitHub
GITHUB_EXCEL_URL = os.getenv("GITHUB_EXCEL_URL", "")

# Formato da data de processamento
DATA_PROCESSAMENTO = os.getenv("DATA_PROCESSAMENTO")

# Configurações AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

# Outros parâmetros de configuração podem ser adicionados aqui conforme necessário
RAW_PATH = f"s3://{S3_BUCKET}/raw/"
STAGE_PATH = f"s3://{S3_BUCKET}/stage/"
ANALYTICS_PATH = f"s3://{S3_BUCKET}/analytics/"
RAW_CLIENTES = RAW_PATH + "clientes/"
RAW_ENDERECOS = RAW_PATH + "enderecos/"
STAGE_CLIENTES = STAGE_PATH + "clientes/"
STAGE_ENDERECOS = STAGE_PATH + "enderecos/"
ANALYTICS_CLIENTES = ANALYTICS_PATH + "clientes/"