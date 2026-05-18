# TERRAFORM OUTPUTS

output "cluster_name" {
  value       = aws_eks_cluster.eks_cluster.name
  description = "The name of the EKS cluster to configure kubectl and authenticate"
}

output "cluster_endpoint" {
  value       = aws_eks_cluster.eks_cluster.endpoint
  description = "The URL endpoint for the Kubernetes API server on your EKS cluster"
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.eks_api_repo.repository_url
  description = "The registry URL string used to tag and push Docker images to ECR"
}

output "region" {
  value       = var.region
  description = "The AWS region where all resources were provisioned"
}