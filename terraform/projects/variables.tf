variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID (region-specific)"
  type        = string
}

variable "key_name" {
  description = "Name of your existing EC2 key pair"
  type        = string
}