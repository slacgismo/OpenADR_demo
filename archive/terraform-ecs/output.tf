
output "api_endpoint" {
  value = aws_lb.vtn.dns_name
}
