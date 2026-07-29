aws glue create-crawler \
  --name "crawler-raw" \
  --role #ROLE \
  --database-name "db_projeto_puc" \
  --targets S3Targets=[{Path="s3://projeto-puc-fraud-prevention/raw/"}] \
