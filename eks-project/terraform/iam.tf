# ROLE 1: EKS Cluster Role

# 1.1 Create the IAM Role for the EKS Control Plane
resource "aws_iam_role" "eks_cluster_role" {
  name = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.cluster_name}-cluster-role"
  }
}

# 1.2 Attach AmazonEKSClusterPolicy to the Cluster Role
resource "aws_iam_role_policy_attachment" "cluster_policy_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}



# ROLE 2: EKS Node Group Role


# 2.1 Create the IAM Role for the Worker Nodes (EC2)
resource "aws_iam_role" "eks_node_role" {
  name = "${var.cluster_name}-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.cluster_name}-node-role"
  }
}

# 2.2 Attach AmazonEKSWorkerNodePolicy to the Node Role
resource "aws_iam_role_policy_attachment" "worker_node_policy_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}

# 2.3 Attach AmazonEKS_CNI_Policy to the Node Role (Handles Pod networking)
resource "aws_iam_role_policy_attachment" "cni_policy_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}

# 2.4 Attach AmazonEC2ContainerRegistryReadOnly to the Node Role (Allows pulling images from ECR)
resource "aws_iam_role_policy_attachment" "ecr_read_only_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}