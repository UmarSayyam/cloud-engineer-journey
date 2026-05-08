variable "instance_type" {
    description = "variable for instance type"
    type        = string
    default     = "t3.micro"
}

variable "environment" {
  description = "variable for environment"
  type = string
  default = "dev"
}