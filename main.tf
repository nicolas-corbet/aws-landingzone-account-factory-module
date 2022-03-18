data "aws_organizations_organization" "organization" {}

data "aws_organizations_organizational_units" "ou" {
  parent_id = data.aws_organizations_organization.organization.roots[0].id
}

resource "aws_organizations_account" "account" {
  name      = var.account_friendly_name
  email     = var.account_email_address
  parent_id = data.aws_organizations_organizational_units.ou.children[index(data.aws_organizations_organizational_units.ou.children[*].name, var.account_organization_ou)].id
}

resource "time_sleep" "wait_60_seconds" {
  depends_on      = [aws_organizations_account.account]
  create_duration = "60s"
}

resource "aws_iam_account_alias" "alias" {
  depends_on    = [time_sleep.wait_30_seconds]
  provider      = aws.account
  account_alias = var.account_alias
}

resource "null_resource" "default_vpc_removal" {
  depends_on = [time_sleep.wait_30_seconds]
  provisioner "local-exec" {
    interpreter = ["bash", "-c"]
    working_dir = path.module
    command     = <<EOF
set -e
CREDENTIALS=(`aws sts assume-role \
  --role-arn "arn:aws:iam::${aws_organizations_account.account.id}:role/${var.automation_role_name}" \
  --role-session-name "terraform-landing_zone" \
  --query "[Credentials.AccessKeyId,Credentials.SecretAccessKey,Credentials.SessionToken]" \
  --output text`)

unset AWS_PROFILE
export AWS_DEFAULT_REGION=${var.default_region}
export AWS_ACCESS_KEY_ID="$${CREDENTIALS[0]}"
export AWS_SECRET_ACCESS_KEY="$${CREDENTIALS[1]}"
export AWS_SESSION_TOKEN="$${CREDENTIALS[2]}"

aws sts get-caller-identity
python scripts/default_vpc_removal.py
EOF
  }
}