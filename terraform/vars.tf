## Name for lambda1
variable "lambda1_name" {
  type = string
  default = "lambda1"
}

## Source directory for lambda1
variable "lambda1_source_dir" {
    type = string
    default = "../terraform-remote-deployment/lambda1"
}