terraform {
  backend "s3" {
    bucket         = "ahmed-fullproject-tfstate-2026"
    key            = "full-project/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
