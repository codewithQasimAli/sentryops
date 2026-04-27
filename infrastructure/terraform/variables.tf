variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-central-1"
}

variable "ami_id" {
  description = "Ubuntu 22.04 LTS AMI for eu-central-1"
  type        = string
  default     = "ami-0faab6bdbac9486fb"
}

variable "key_name" {
  description = "EC2 Key Pair name"
  type        = string
  default     = "sentryops-key"
}
