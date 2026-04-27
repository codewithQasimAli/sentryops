output "instance_public_ip" {
  description = "Public IP address of the SentryOps EC2 instance"
  value       = aws_instance.sentryops_ec2.public_ip
}

output "instance_public_dns" {
  description = "Public DNS of the SentryOps EC2 instance"
  value       = aws_instance.sentryops_ec2.public_dns
}

output "sentryops_url" {
  description = "SentryOps application URL"
  value       = "http://${aws_instance.sentryops_ec2.public_ip}:8000/api/v1/health"
}
