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

# ✅ الحل الجذري: يمنع "yes" وأي قيم غلط
variable "docker_image" {
  type        = string
  description = "Docker image to deploy in form repo/image:tag (e.g. ahmeduioueu235g/myapp:latest)"

  validation {
    condition = (
      length(trimspace(var.docker_image)) > 0 &&
      can(regex("^[a-z0-9]+([._-][a-z0-9]+)*/[a-z0-9]+([._-][a-z0-9]+)*:[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", trimspace(var.docker_image)))
    )
    error_message = "docker_image must be like 'repo/image:tag' (example: ahmeduioueu235g/myapp:latest)."
  }
}

variable "container_name" {
  type        = string
  description = "Docker container name"
  default     = "myapp"
}

variable "container_port" {
  type        = number
  description = "Port inside the container"
  default     = 5000
}

variable "app_port" {
  type        = number
  description = "Port exposed on EC2"
  default     = 80
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

variable "public_key" {
  type        = string
  description = "SSH public key content (optional)"
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
  description = "CIDR allowed to SSH"
  default     = "0.0.0.0/0"
}
