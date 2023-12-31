terraform {
  required_version = "~> 1.6.6"

  backend "s3" {
    bucket         = "terraform-state-146479615822"
    key            = "global/s3/datapipeline.tfstate"
    region         = "us-east-1"
    dynamodb_table = "dynamodb-terraform-state-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.29.0"
    }
    http = {
      source  = "hashicorp/http"
      version = "3.3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Name = local.project_name
    }
  }
}