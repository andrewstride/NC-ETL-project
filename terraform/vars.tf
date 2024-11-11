variable "lambda1_name" {
  type = string
  default = "lambda1"
}

variable "lambda1_source_file" {
    type = string
    default = "${path.module}/../src/lambda1.py"
}