# RESOURCE 1: EKS Cluster Control Plane

resource "aws_eks_cluster" "eks_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids             = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
    endpoint_public_access = true
  }

  # Ensure IAM Role policies are created before the EKS cluster starts initializing
  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy_attach
  ]
}

# RESOURCE 2: EKS Managed Node Group

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "eks-demo-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
  instance_types  = [var.node_instance_type]

  scaling_config {
    desired_size = var.desired_nodes
    min_size     = 1
    max_size     = 3
  }

  # Ensure IAM Node policies are active so worker nodes can join the cluster and pull from ECR
  depends_on = [
    aws_iam_role_policy_attachment.worker_node_policy_attach,
    aws_iam_role_policy_attachment.cni_policy_attach,
    aws_iam_role_policy_attachment.ecr_read_only_attach
  ]
}