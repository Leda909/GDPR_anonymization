# Source bucket that need to be anonymized
resource "aws_s3_bucket" "plain_data_bucket" {
  bucket = "gdpr-source-data-bucket-${random_id.id.hex}"
  tags={
    Name="GDPR Source Data"
  }
}

# Destination bucket for anonymized data - Not necessery - For testing purpose
resource "aws_s3_bucket" "obfuscated_data_bucket" {
  bucket = "gdpr-obfuscated-data-bucket-${random_id.id.hex}"
  tags={
    Name="GDPR Obfuscated Data"
  }
}

# Generate random id for bucket names to ensure uniqueness
resource "random_id" "id" {
  byte_length = 4
}