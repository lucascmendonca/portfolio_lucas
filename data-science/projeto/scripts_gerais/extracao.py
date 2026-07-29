import sys
import os
import boto3
import requests

# Configurações
GIT_USER = "lucascmendonca" # Seu usuario do git
BUCKET = "projeto-puc-fraud-prevention"
RAW_PREFIX = "raw/"
ZIP_FILENAME = "credit_risk_dataset.csv.zip"

# URL do ZIP no GitHub (link direto para o arquivo)
GITHUB_ZIP_URL = f"https://raw.githubusercontent.com/{GIT_USER}/eixo5_grupo3_20252/main/projeto/base_dados/credit_risk_dataset.csv.zip"

def main():
    # Baixar arquivo do GitHub
    print("Baixando ZIP do GitHub...")
    response = requests.get(GITHUB_ZIP_URL)
    if response.status_code != 200:
        raise Exception(f"Erro ao baixar arquivo: {response.status_code}")
    
    # Salvar em /tmp/
    local_path = f"/tmp/{ZIP_FILENAME}"
    with open(local_path, "wb") as f:
        f.write(response.content)
    print(f"Arquivo salvo temporariamente em {local_path}")

    # Enviar para o S3
    s3 = boto3.client("s3")
    s3.upload_file(local_path, BUCKET, f"{RAW_PREFIX}{ZIP_FILENAME}")
    print(f"Arquivo enviado para s3://{BUCKET}/{RAW_PREFIX}{ZIP_FILENAME}")

if __name__ == "__main__":
    main()
