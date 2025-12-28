# read the lambda handler file from src folder to zip and upload to obfuscator lambda
data "archive_file" "obfuscator_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../src/obfuscator.py"
  output_path = "${path.module}/../deployment/obfuscator_lambda.zip"
}

# create the obfuscator lambda function
resource "aws_lambda_function" "gdpr_obfuscator_lambda" {
  filename      = data.archive_file.obfuscator_lambda_zip.output_path
  function_name = "gdpr_obfuscator_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "obfuscator.lambda_handler"   # file_name.function_name
  runtime       = "python3.12"
  # set memory size and timeout
  memory_size = 512
  timeout     = 60
  
  # awswrangler layer for data obfuscation lambda
  layers = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:17"]
  
  # compute the source code hash for the lambda function
  source_code_hash = data.archive_file.obfuscator_lambda_zip.output_base64sha256

  # Set environment variables for the Lambda function to save obfuscated data. 
  # This is optional for testing.
  environment {
    variables = {
          DESTINATION_BUCKET = aws_s3_bucket.obfuscated_data_bucket.bucket
          PII_FIELDS = join(",", var.pii_fields)
      }
  }
}