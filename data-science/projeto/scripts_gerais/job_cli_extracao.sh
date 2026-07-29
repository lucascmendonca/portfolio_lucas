aws glue create-job \
  --name "extracao-job" \
  --role # ROLE ACCESS \
  --command "Name=pythonshell,ScriptLocation=s3://projeto-puc-fraud-prevention/scripts/extracao_zip.py,PythonVersion=3" \
  --default-arguments '{"--job-language":"python"}' \
  --max-capacity 1
