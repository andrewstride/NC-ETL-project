provider "aws" {
    region = "eu-west-2"
}

terraform {

## Backend bucket to store the Terraform state
backend "s3" {
    bucket = "ncterraformers-state-bucket"
    key = "terraform.tfstate"
    region = "eu-west-2"
}
}