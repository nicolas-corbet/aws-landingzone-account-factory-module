terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.7.2"
    }
  }
}

# Provider in created account

provider "aws" {
  region = var.default_region
  alias  = "account"
  assume_role {
    role_arn     = "arn:aws:iam::${aws_organizations_account.account.id}:role/${var.automation_role_name}"
    session_name = "terraform-landing_zone"
  }
  default_tags {
    tags = {
      Author = "Nicolas Corbet"
    }
  }
}
