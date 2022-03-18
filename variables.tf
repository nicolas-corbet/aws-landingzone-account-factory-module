variable "default_region" {
  type = string
}

variable "account_friendly_name" {
  type = string
}

variable "account_organization_ou" {
  type = string
}

variable "account_email_address" {
  type = string
}

variable "account_alias" {
  type = string
}

variable "automation_role_name" {
  type    = string
  default = "automation_role"
}