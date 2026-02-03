variable "project_name" {
  type        = string
  description = "Name tag for resources"
  default     = "devops-project"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "eu-central-1"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t3.micro"
}

variable "docker_image" {
  type        = string
  description = "Docker image on Docker Hub"
  default     = "ahmeduioueu235g/myapp:1.0"
}

variable "container_name" {
  type        = string
  description = "Docker container name on the EC2 instance"
  default     = "myapp"
}

variable "container_port" {
  type        = number
  description = "Port inside the container (Flask)"
  default     = 5000
}

variable "app_port" {
  type        = number
  description = "Port exposed on the EC2 instance (public)"
  default     = 9090
}

variable "key_name" {
  type        = string
  description = "EC2 Key Pair name to create"
  default     = "devops-project-key"
}

variable "public_key_path" {
  type        = string
  description = "Path to your SSH public key file"
  default     = "~/.ssh/id_rsa.pub"
}

variable "allow_ssh" {
  type        = bool
  description = "Allow SSH access (22)"
  default     = true
}

variable "ssh_cidr" {
  type        = string
  description = "CIDR allowed to SSH (better: your_public_ip/32)"
  default     = "0.0.0.0/0"
}
