# Configure the AWS Provider and an S3 Backend for Terraform State
terraform {
  required_providers {
    aws={
      source="hashicorp/aws"
      version="~> 5.0"
    }
    
  }
  backend "s3" {
    bucket = "s3-obfuscator-terraform-state"
    key    = "folder/terraform-state-file"
    region = var.region
  }

}

provider "aws" {
  region = var.region
}