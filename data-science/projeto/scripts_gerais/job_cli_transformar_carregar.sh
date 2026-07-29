aws glue create-job \
  --name "transformacao-job" \
  --role #ROLE ACCESS \
  --command "Name=glueetl,ScriptLocation=s3://projeto-puc-fraud-prevention/scripts/transformacao_carga.py,PythonVersion=3" \
  --glue-version "3.0" \
  --default-arguments '{"--job-language":"python"}' \
  --max-capacity 2