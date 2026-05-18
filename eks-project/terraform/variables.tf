variable "cluster_name" {
  type = string
  default = "eks-demo"
  description = "The name of EKS cluster"
}

variable "region" {
  type = string
  default = "ap-south-1"
  description = "The AWS region where resources will be deployed"
}

variable "node_instance_type" {
  type = string
  default = "t3.medium"
  description = "The EC2 instance type for the EKS worker nodes"
}

variable "desired_nodes" {
  type = number
  default = 2
  description = "The desired number of woker node in EKS node group"
}