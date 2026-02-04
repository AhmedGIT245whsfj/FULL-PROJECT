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
  description = "Docker image to deploy in form repo/image:tag (e.g. ahmeduioueu235g/myapp:sha-abcdef1)"

  validation {
    condition = (
      length(trimspace(var.docker_image)) > 0 &&
      can(regex("^[a-z0-9]+([._-][a-z0-9]+)*/[a-z0-9]+([._-][a-z0-9]+)*:[A-Za-z0-9][A-Za-z0-9._-]{0,127}$", trimspace(var.docker_image)))
    )
    error_message = "docker_image must be like 'repo/image:tag' (example: ahmeduioueu235g/myapp:sha-abcdef1)."
  }
}

variable "deploy_version" {
  type        = string
  description = "Deployment version identifier (commit SHA, tag, etc.)"
  default     = ""

  validation {
    condition = (
      trimspace(var.deploy_version) == "" ||
      can(regex("^[0-9a-f]{40}$", trimspace(var.deploy_version))) ||
      can(regex("^[0-9a-f]{7,40}$", trimspace(var.deploy_version))) ||
      can(regex("^sha-[0-9a-f]{7}$", trimspace(var.deploy_version))) ||
      can(regex("^[0-9]+\\.[0-9]+\\.[0-9]+$", trimspace(var.deploy_version)))
    )
    error_message = "deploy_version should be a git SHA (7-40 hex), full SHA (40), 'sha-xxxxxxx', or semver like 1.2.3 (or empty)."
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

# ✅ Guardrail اختياري: لو فعلته يمنع 0.0.0.0/0 على SSH
variable "strict_security" {
  type        = bool
  description = "If true, block dangerous SSH cidr (0.0.0.0/0) when allow_ssh=true"
  default     = false
}

variable "ssh_guardrail" {
  type        = bool
  description = "Internal guardrail variable (do not set). Used only for validation."
  default     = true

  validation {
    condition = (
      var.ssh_guardrail == true &&
      (
        var.strict_security == false ||
        var.allow_ssh == false ||
        (trimspace(var.ssh_cidr) != "0.0.0.0/0")
      )
    )
    error_message = "Security guardrail: strict_security=true + allow_ssh=true requires ssh_cidr to NOT be 0.0.0.0/0 (use your_ip/32)."
  }
}
