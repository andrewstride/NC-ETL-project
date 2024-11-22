## Exclude following directories from Lambda compilation
variable "lambda_comp_exclude_list" {
    type = list(string)
    default = ["test", "src/__pycache__", ".pytest_cache"]
}

## Name for lambda1
variable "lambda1_name" {
  type = string
  default = "lambda1"
}

## Deployment directory for lambda1
variable "lambda1_deployment_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda1"
}

## Deployment directory for lambda1 layer
variable "lambda1_layer_deployment_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda1-layer"
}

## Source directory for lambda1
variable "lambda1_source_dir" {
    type = string
    default = "../python/lambda1"
}


## Name for lambda2
variable "lambda2_name" {
  type = string
  default = "lambda2"
}

## Deployment directory for lambda2
variable "lambda2_deployment_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda2"
}

## Deployment directory for lambda2 layer
variable "lambda2_layer_deployment_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda2-layer"
}

## Source directory for lambda2
variable "lambda2_source_dir" {
    type = string
    default = "../python/lambda2"
}

## Name for lambda3
variable "lambda3_name" {
    type = string
    default = "lambda3"
}

## Deployment directory for lambda3
variable "lambda3_deployment_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda3"
}

## Deployment directory for lambda3 layer
variable "lambda3_layer_deployment_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda3-layer"
}

## Source directory for lambda3
variable "lambda3_source_dir" {
    type = string
    default = "../python/lambda3"
}