<!-- BEGIN_TF_DOCS -->



## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_alias"></a> [account_alias](#input_account_alias) | n/a | `string` | n/a | yes |
| <a name="input_account_email_address"></a> [account_email_address](#input_account_email_address) | n/a | `string` | n/a | yes |
| <a name="input_account_friendly_name"></a> [account_friendly_name](#input_account_friendly_name) | n/a | `string` | n/a | yes |
| <a name="input_account_organization_ou"></a> [account_organization_ou](#input_account_organization_ou) | n/a | `string` | n/a | yes |
| <a name="input_default_region"></a> [default_region](#input_default_region) | n/a | `string` | n/a | yes |
| <a name="input_automation_role_name"></a> [automation_role_name](#input_automation_role_name) | n/a | `string` | `"automation_role"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_account_id"></a> [account_id](#output_account_id) | n/a |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider_aws) | >= 4 |
| <a name="provider_aws.account"></a> [aws.account](#provider_aws.account) | >= 4 |
| <a name="provider_null"></a> [null](#provider_null) | n/a |
| <a name="provider_time"></a> [time](#provider_time) | 0.7.2 |

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement_terraform) | >= 1.0 |
| <a name="requirement_aws"></a> [aws](#requirement_aws) | >= 4 |
| <a name="requirement_time"></a> [time](#requirement_time) | 0.7.2 |


<!-- END_TF_DOCS -->