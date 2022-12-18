
output "ec2_host" {
  value = aws_instance.ec2.public_dns
}