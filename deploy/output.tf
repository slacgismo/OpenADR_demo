
output "ec2_host" {
  value = aws_instance.bastion.public_dns
}