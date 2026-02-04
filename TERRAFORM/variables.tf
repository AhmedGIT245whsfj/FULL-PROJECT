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
  default     = "t3.micro" # خليها t2.micro عشان free tier في العادة
}

variable "docker_image" {
  type        = string
  description = "Docker image to deploy (passed from CI/CD), e.g. ahmeduioueu235g/myapp:1.0.1"
  # ✅ مفيش default عشان GitHub Actions يبعت النسخة
}

variable "container_name" {
  type        = string
  description = "Docker container name on the EC2 instance"
  default     = "myapp"
}

variable "container_port" {
  type        = number
  description = "Port inside the container"
  default     = 5000
}

variable "app_port" {
  type        = number
  description = "Port exposed on the EC2 instance"
  default     = 9090
}

variable "key_name" {
  type        = string
  description = "EC2 Key Pair name to create"
  default     = "devops-project-key"
}

variable "public_key_path" {
  type        = string
  description = "Path to your SSH public key file (used when public_key is empty)"
  default     = "~/.ssh/id_rsa.pub"
}

variable "public_key" {
  type        = string
  description = "SSH public key content (preferred in CI); overrides public_key_path when set"
  default     = ""

  validation {
    condition     = trimspace(var.public_key) != "" || fileexists(pathexpand(var.public_key_path))
    error_message = "Provide public_key or ensure public_key_path exists."
  }
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
