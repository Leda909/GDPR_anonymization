# Launchpad GDPR Obfuscator Service | Anonymizator ETL pipeline

The GDPR Obfuscator is an automated security tool designed to protect Personally Identifiable Information (PII) during data ingestion into AWS. This service ensures compliance with GDPR standards by intercepting files as they land in an S3 bucket and masking sensitive data before it is used for bulk analysis.

### Key features:

* **Multi-Format Support:** Handles CSV, JSON, and Parquet files.
* **Anonymization:** Replaces sensitive data (e.g., names, emails) with masked strings (*****) while preserving the original file structure.
* **Infrastructure as Code:** Fully automated deployment using CI/CD Github Action and Terraform to ensure a reproducible environment within the AWS ecosystem.
* **Performance:** Optimized to handle files up to 1MB in under 60 seconds using the AWSSDKPandas Lambda layer.
* **Event-Driven:** Automatically triggers via Amazon EventBridge when new files are uploaded.
* **High Performance:** Process files up to 1MB in under 60 seconds to ensure efficient data pipelines.

### How it Works:
The service follows the "Anonymization at Ingestion" pattern:

* **Ingestion:** A file lands in the source S3 bucket
* **Trigger:** EventBridge captures an ObjectCreated event and sends a JSON event to the Lambda function.
* **Processing:** The Lambda function reads the file into a memory-efficient Pandas DataFrame using awswrangler. It identifies PII columns defined in the configuration. 
* **Obfuscation:** The tool identifies (Pii) columns specified in the configuration and replaces sensitive values with a fixed mask while maintaining the original data structure and file schema. The resulting stream is saved to the destination S3 bucket, ensuring no sensitive data is persisted in temporary Lambda storage.
* **Audit:** All actions monitored and potential errors are logged to AWS CloudWatch: All processing logs, including success metrics and error traces, are available in the /aws/lambda/gdpr_obfuscator log group. Error Handling: If an unsupported file type or corrupted file is uploaded, the service logs a descriptive error message without crashing the pipeline.

### Customizing Obfuscation
You can define which fields to hide without changing the Python code. Edit the terraform/terraform.tfvars file. Please, see example_terraform.tfvars:

```bash
region             = "your-aws-region"
pii_fields         = ["name", "email_address", "phone_number"] - etc.
```
## AWS Architecture Diagram

<img src="./assets/archit_diag.png" style="width: 40%;">

### Project Sources & Compliance

* GDPR Requirement: All (PII) data that could identify an individual must be anonymized. [*****]
* Data Integrity: Output files maintain the exact structure of the input, replacing only specified PII fields.
* Security: Codebase audited for vulnerabilities; zero hardcoded credentials.
* PEP-8: 100% compliance.
* Scalability: Tested for files up to 1MB; Runtime < 60s.
* Dynamic Configuration: Uses terraform.tfvars to allow users to customize bucket names, environment tags, and PII field lists without changing the core code.

## Technologies and packages

<p align="center">
    <!-- Python -->
    <a href="https://www.python.org/" target="_blank" rel="noreferrer" style="margin: 25px;">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="100px" height="100px"/>
    </a>
    <!-- Terraform -->
    <a href="https://www.terraform.io/" target="_blank" rel="noreferrer" style="margin: 25px;">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/terraform/terraform-original.svg" alt="terraform" width="100px" height="100px"/>
    </a>
    <!-- Amazon -->
    <a href="https://aws.amazon.com/" target="_blank" rel="noreferrer" style="margin: 25px;">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_6owgj8w4Bpwc1q2BNQdQ0z_LqBLw-XB0Fg&s" alt="aws" width="100px" height="100px"/>
    </a>
    <!-- Github Action -->
    <a href="https://github.com/features/actions" target="_blank" rel="noreferrer" style="margin: 25px;">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeELfqnsZAFa7QU00kjkio5nwkEP9uilZVyg&s" alt="github actions" width="100px" height="100px"/>
    </a>
    <!-- Git -->
    <a href="https://git-scm.com/" target="_blank" rel="noreferrer" style="margin: 25px;">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="git" width="100px" height="100px"/>
    </a>
</p>

<!-- Python packages list -->
### Python packages:
<ul>
    <li>boto3 1.38.24</li>
    <li>awswrangler 3.12.0</li>
    <li>pandas 2.3.0</li>
    <li>pytest 8.3.5</li>
    <li>moto </li>
</ul>

## Installation & Setup (Local)

1. Clone the Repository<br>
    ```bash
    git clone https://github.com/Leda909/GDPR_Obfuscator
    cd GDPR_Obfuscator
    ```

2. Environment Setup<br>

    ### On Windows:
    Please, see detailed guide in *assets/windows.md* file.

    ### On Linux | MacOs
    IMPORTANT! Github CI/CD runs in Linux, hence you can use the makefile made for Linux system.

    * Create a virtual environment:<br>
    `python -m venv venv`

    * Activate your venv:<br>
    `source venv/bin/activate`

    * Install packages: 
    Required packages are listed in requirements.txt and can be installed using the makefile.<br>
    `make requirements`

3. Set up your **AWS CREDENTIALS**

    To use AWS services and infrastructure, sign up to a AWS account and create a IAM user. Once this is done, extract your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.

    Run the following in your VS terminal:

    ```bash
    export AWS_ACCESS_KEY_ID = <your key id>
    export AWS_SECRET_ACCESS_KEY = <your secret access key>
    export AWS_DEFAULT_REGION = <your default region>
    ```

4. Create Remote S3 Backend bucket for terraform.state files (One-time Bootstrap)<br>

    Create the S3 bucket for the Terraform state file to allow for team collaboration and CI/CD:

    For creating the S3 backend bucket, run in terminal:
    ```bash
    aws s3api create-bucket \
        --bucket s3-obfuscator-terraform-state \
        --region eu-west-2 \
        --create-bucket-configuration LocationConstraint=eu-west-2
    ```

    Enable Versioning on it (Recommended). Run in terminal:
    ```bash
    aws s3api put-bucket-versioning \
        --bucket s3-obfuscator-terraform-state \
        --versioning-configuration Status=Enabled
    ```

5. Deploy Infrastructure by Terraform<br>(Run the following commands step by step in the terminal):

    * `cd terraform`

    * `terraform init`

    * `terraform plan`

    * `terraform apply`

## Remote Installation

1. Simply fork this repo and Configure your AWS credentials in **GitHub Secrets**.

2. Navigate to your repository **Settings > Secrets and variables > Actions**.

Add the following New repository secrets:

```bash
AWS_ACCESS_KEY_ID: Your AWS access key.
AWS_SECRET_ACCESS_KEY: Your AWS secret key.
```
Uncomment the terraform part in the ylm file until destroy. Then, AWS Deployment and Python Tests automatically will be run by Github Action ylm | CI/CD file on every occation you push into your main branch. When you finished using AWS `terraform destroy` everything to avoid unexpected expenses.

## Running Tests
Note: Tests use moto to mock AWS, so no real AWS charges are incurred during testing.

Please, for Windows OS, see: *assets/windows.md* file.

For Linux | Mac OS:

* Activate venv:<br>
`source venv/bin/activate`

* Add the given PYTHONPATH to your environment variables:<br>
`export PYTHONPATH=$(pwd)`

* To run tests, run the following command:<br>
`make unit-test`

* To run all checks (tests, linting, security), run the following command:<br>
`make run-checks`

* To create a coverage test, run:<br>
`make check-coverage-txt`

## Live Integration Testing - Usage

Once deployed, you can verify the EventBridge trigger -monitors the ingestion/source S3 bucket for Object Created events - and Lambda function using the AWS CLI. When run *terraform apply*, save the ingestion/source and the destination *S3 bucket names* from terraform output!

1. Upload a Supported File (CSV) to ingestion S3 bucket, (run in terminal in the root folder):<br>
`aws s3 cp data/test/sample.csv s3://your-ingestion-bucket-name/`

2. Upload an Unsupported File (TXT) to ingestion S3 bucket<br>
`aws s3 cp data/test/sample.txt s3://your-ingestion-bucket-name/`

3. Check the Results<br>
Wait a few seconds for the Lambda to finish, then check the destination bucket. It should only include the supported file after obfuscating. <br>
`aws s3 ls s3://your-processed-bucket-name/ --recursive`
To download the all obfuscated files from aws S3 destination/obfuscated folder (it will create a local folder of local_obfuscated), use:<br>
`aws s3 sync s3://your-processed-bucket-name/obfuscated/ ./data/local_obfuscated`

#### Expected outcome: 
Sould be only the sample.csv.

Example sample.csv
```bash
student_id, name, email_address
1234, John Smith, j.smith@email.com
```

Example Obfuscated sample.csv
```bash
student_id, name, email_address
1234, *****, *****
```

## Resources

Amazon S3 can send events to Amazon EventBridge whenever certain events (eg. Object Created) happen in your bucket.
The format of the events; JSON schema.
* [Amazon S3 event notifications on EventBridge](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html)

* [EventBridge event message structure is Json format](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ev-events.html)

* [YouTube - How to Install ASW SDK For Pandas on AWS Lambda Function](https://www.youtube.com/watch?v=Ofwblf_K408&t=46s)

* [awswranggler](https://aws-sdk-pandas.readthedocs.io/en/3.2.1/stubs/awswrangler.s3.read_csv.html)