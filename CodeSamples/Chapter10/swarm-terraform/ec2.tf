data "aws_ami" "ubuntu_focal" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/nvm-ssd/ubuntu-bionic-20.04-amd64-server"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}


resource "aws_vpc" "swarm_cluster_vpc" {
  cidr_block           = "172.20.1.0/24"
  enable_dns_hostnames = true

}

resource "aws_internet_gateway" "main_gateway" {
  vpc_id = aws_vpc.swarm_cluster_vpc.id
}

resource "aws_route_table" "public_internet_access" {
  vpc_id = aws_vpc.swarm_cluster_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_gateway.id
  }
}

resource "aws_security_group" "swarm_security_group" {
  name        = "swarm security group"
  description = "Swarm Security Group"
  vpc_id      = aws_vpc.swarm_cluster_vpc.id

  ingress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "Allow HTTPS inbound"
    from_port        = 0
    ipv6_cidr_blocks = ["::/0"]
    prefix_list_ids  = ["value"]
    protocol         = "tcp"
    security_groups  = ["value"]
    self             = false
    to_port          = 443
  }]


  egress = [{
    cidr_blocks = ["0.0.0.0/0"]
    description = "allow all"
    protocol    = -1
    from_port   = 0
    to_port     = 0
  }]


}

resource "aws_security_group" "foobar" {
}

resource "aws_instance" "swarm_cluster" {
  count         = var.swarm_node_count
  ami           = data.aws_ami.ubuntu_focal.id
  instance_type = var.ec2_instance_type

  vpc_security_group_ids = [aws_security_group.swarm_security_group.id]
  key_name               = var.ec2_key_name

  root_block_device {
    volume_type = "gp2"
    volume_size = "20" # GiB
    encrypted   = true
  }
}
