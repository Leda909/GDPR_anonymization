import pytest
import boto3
import awswrangler as wr
import pandas as pd
import os
import hcl2
from moto import mock_aws
from src.obfuscator import lambda_handler

@pytest.fixture(scope='function')
def s3_client():
    """Yields a mocked S3 client."""
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-2")

@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

# @pytest.fixture(scope='module')
def get_pii_from_terraform():
    with open('terraform/terraform.tfvars', 'r') as f:
        tf_vars = hcl2.load(f)
        #'pii_fields' is a list in the tfvars file
        return ",".join(tf_vars['pii_fields'])

@mock_aws
class TestObfuscator:
    def test_lambda_obfuscates_local_csv_file(self, s3_client):
        # 1a. SETUP: Mock Buckets
        source_bucket = "gdpr-source-data-bucket-test"
        dest_bucket = "gdpr-obfuscated-data-bucket-test"
        
        s3_client.create_bucket(Bucket=source_bucket, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})
        s3_client.create_bucket(Bucket=dest_bucket, CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'})

        # 1b. Configure Environment variables for the Lambda function
        os.environ["DESTINATION_BUCKET"] = dest_bucket
        # Configure PII fields for dummy.csv has 'name' and 'email_address'
        os.environ["PII_FIELDS"] = get_pii_from_terraform()

        # 2. SEED: Load your ACTUAL local file and upload it to the mock S3
        source_key = "dummy.csv"
        local_file_path = f"data/raw/{source_key}"

        # Ensure the directory exists to avoid FileNotFoundError during the test
        if not os.path.exists(local_file_path):
            pytest.fail(f"Local test file not found at {local_file_path}. Please create it first.")
            
        df_local = pd.read_csv(local_file_path)
        wr.s3.to_csv(df_local, f"s3://{source_bucket}/{source_key}", index=False)

        # 3. ACT: Trigger the handler with EventBridge style event
        mock_event = {
            "detail": {
                "bucket": {"name": source_bucket},
                "object": {"key": source_key}
            }
        }
        
        lambda_handler(mock_event, None)

        # 4. ASSERT: Read the result from the destination bucket
        result_df = wr.s3.read_csv(f"s3://{dest_bucket}/obfuscated/{source_key}")

        # 5. If not exsist, create the local "obfuscated" folder, and save the result there
        output_dir = "data/obfuscated"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save the result locally for manual inspection
        output_path = os.path.join(output_dir, "obfuscated_result.csv")
        result_df.to_csv(output_path, index=False)
        
        print(f"\nSuccess! Find the Obfuscated file here: {output_path}")

        # 6. ASSERT: Validate that PII fields are obfuscated
        # Check that PII fields are masked
        # Check the columns defined in PII_FIELDS env variable as written in terraform.tfvars - hardcoded here for clarity
        for col in ["name", "email_address"]:
            if col in result_df.columns:
                assert all(result_df[col] == "*****"), f"Column {col} was not obfuscated"
        
        # Check that one non-PII field (e.g., student_id) is still the same as the original
        if "student_id" in result_df.columns:
            assert result_df["student_id"][0] == df_local["student_id"][0]



