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
