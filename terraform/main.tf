# 1. Setup the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2" # Oregon is common for tech, but "us-east-1" works too
}

# 2. Create a Virtual Private Cloud (VPC)
resource "aws_vpc" "carbon_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "forest-carbon-vpc"
  }
}

# 3. Create a Public Subnet for the API
resource "aws_subnet" "carbon_subnet" {
  vpc_id                  = aws_vpc.carbon_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

# 4. ECS Cluster
resource "aws_ecs_cluster" "carbon_cluster" {
  name = "forest-carbon-cluster"
}

# 5. Task Definition (The blueprint for your Docker container)
resource "aws_ecs_task_definition" "carbon_task" {
  family                   = "forest-carbon-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256" # Minimal CPU for cost-efficiency
  memory                   = "512" # Minimal RAM

  container_definitions = jsonencode([
    {
      name      = "forest-carbon-api"
      image     = "YOUR_DOCKER_IMAGE_URL" # We will fill this once you push to ECR
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      environment = [
        { name = "OPENAI_API_KEY", value = "REPLACE_WITH_AWS_SECRET" }
      ]
    }
  ])
}


resource "aws_security_group" "api_sg" {
  name   = "carbon-api-sg"
  vpc_id = aws_vpc.carbon_vpc.id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open to the world (standard for portfolio demos)
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

