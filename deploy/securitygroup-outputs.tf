# AWS EC2 Security Group Terraform Outputs

# Public Bastion Host Security Group Outputs

## private OpenADR Security Group Outputs
output "private_openadr_sg_group_name" {
  description = "The name of the security group"
  value       = module.private_openadr_sg.this_security_group_name
}


