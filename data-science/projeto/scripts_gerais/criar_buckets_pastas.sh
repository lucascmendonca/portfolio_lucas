export BUCKET_NAME="projeto-puc-fraud-prevention"
export REGION="us-east-1"
aws s3 mb s3://$BUCKET_NAME --region $REGION
aws s3api put-object --bucket $BUCKET_NAME --key raw/
aws s3api put-object --bucket $BUCKET_NAME --key processed/
aws s3api put-object --bucket $BUCKET_NAME --key scripts/
aws s3 ls s3://$BUCKET_NAME --recursive
echo "Bucket criado: $BUCKET_NAME"