# to get the S3 source bucket name
output "raw_bucket_name" {
  value = aws_s3_bucket.plain_data_bucket.id
}

# to get the obfuscator lambda function arn
output "lambda_function_arn" {
  value = aws_lambda_function.gdpr_obfuscator_lambda.arn
}