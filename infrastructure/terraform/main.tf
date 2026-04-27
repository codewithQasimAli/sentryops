terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "sentryops_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name    = "sentryops-vpc"
    Project = "sentryops"
  }
}

resource "aws_internet_gateway" "sentryops_igw" {
  vpc_id = aws_vpc.sentryops_vpc.id

  tags = {
    Name    = "sentryops-igw"
    Project = "sentryops"
  }
}

resource "aws_subnet" "sentryops_public_subnet" {
  vpc_id                  = aws_vpc.sentryops_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "sentryops-public-subnet"
    Project = "sentryops"
  }
}

resource "aws_route_table" "sentryops_rt" {
  vpc_id = aws_vpc.sentryops_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.sentryops_igw.id
  }

  tags = {
    Name    = "sentryops-rt"
    Project = "sentryops"
  }
}

resource "aws_route_table_association" "sentryops_rta" {
  subnet_id      = aws_subnet.sentryops_public_subnet.id
  route_table_id = aws_route_table.sentryops_rt.id
}

resource "aws_instance" "sentryops_ec2" {
  ami                    = var.ami_id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.sentryops_public_subnet.id
  vpc_security_group_ids = [aws_security_group.sentryops_sg.id]
  key_name               = var.key_name

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io
    systemctl start docker
    systemctl enable docker
    docker pull ghcr.io/codewithqasimali/sentryops:latest || true
    docker run -d --name sentryops -p 8000:8000 --restart unless-stopped ghcr.io/codewithqasimali/sentryops:latest || true
  EOF

  tags = {
    Name    = "sentryops-ec2"
    Project = "sentryops"
  }
}
