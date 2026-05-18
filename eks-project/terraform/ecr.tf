# RESOURCE : AWS ECR Repository

resource "aws_ecr_repository" "eks_api_repo" {
  name = "eks-api"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "eks-api-repo"
    Project = "eks-project"
  }
}