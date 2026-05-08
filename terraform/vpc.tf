resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = merge(local.common_tags, {
    Name = "umar-terraform-vpc"
  })
}

resource "aws_subnet" "public" {
    vpc_id = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "umar-public-subnet"
  })
}

resource "aws_internet_gateway" "main_igw" {
  vpc_id = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "umar-igw"
  })
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id
  route{
  cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.main_igw.id
  }
  tags = merge(local.common_tags, {
    Name = "umar-public-rt"
  })
}

resource "aws_route_table_association" "public_rta" {
  subnet_id = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.main.id
  name = "web-security-group"
  ingress{
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress{
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress{
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(local.common_tags, {
    Name = "umar-web-sg"
  })
}