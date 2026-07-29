import os
import boto3
import zipfile
from io import BytesIO
from pyspark.sql import SparkSession

# Inicializa Spark
spark = SparkSession.builder.appName("TransformRawToProcessed").getOrCreate()

# Configurações
BUCKET = "projeto-puc-fraud-prevention"
RAW_PREFIX = "raw/"
STAGING_PREFIX = "raw/staging_raw/"
PROCESSED_PREFIX = "processed/"
ZIP_FILENAME = "credit_risk_dataset.csv.zip"

s3 = boto3.resource("s3")
bucket = s3.Bucket(BUCKET)

# Deletar staging_raw/ se existir
print("🔹 Verificando se staging_raw/ existe...")
objs = list(bucket.objects.filter(Prefix=STAGING_PREFIX))
if objs:
    print("staging_raw/ existe, deletando...")
    bucket.objects.filter(Prefix=STAGING_PREFIX).delete()
    print("staging_raw/ deletado.")

# Baixar o zip do S3
zip_obj = s3.Object(BUCKET, f"{RAW_PREFIX}{ZIP_FILENAME}").get()
zip_content = BytesIO(zip_obj['Body'].read())
print(f"Arquivo {ZIP_FILENAME} baixado do S3 com sucesso.")

# Descompactar arquivos diretamente no staging_raw/ do S3
with zipfile.ZipFile(zip_content) as zip_ref:
    for file_info in zip_ref.infolist():
        if not file_info.is_dir():
            file_data = zip_ref.read(file_info.filename)
            s3.Object(BUCKET, f"{STAGING_PREFIX}{file_info.filename}").put(Body=file_data)
            print(f"Arquivo {file_info.filename} enviado para s3://{BUCKET}/{STAGING_PREFIX}{file_info.filename}")

# Listar CSVs na pasta staging_raw/
csv_keys = [obj.key for obj in bucket.objects.filter(Prefix=STAGING_PREFIX) if obj.key.endswith(".csv")]
if not csv_keys:
    raise FileNotFoundError("Nenhum CSV encontrado em staging_raw/.")

print("Arquivos CSV encontrados:", csv_keys)

# Ler CSVs com Spark
s3_paths = [f"s3://{BUCKET}/{key}" for key in csv_keys]
df_raw = spark.read.csv(s3_paths, header=True, inferSchema=True)

# Salvar em Parquet no processed/
output_path = f"s3://{BUCKET}/{PROCESSED_PREFIX}"
df_raw.write.mode("overwrite").parquet(output_path)

print(f"Transformação concluída! Dados salvos em {output_path}")
