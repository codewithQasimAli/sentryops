# SentryOps — Project Context File
*Paste this at the start of every new Claude conversation about this project*

## Who I am
- Name: Qasim Ali
- Degree: BSCS Final Year, SZABIST Karachi
- Background: Cybersecurity (Google cert, Nmap, Wireshark, Metasploit, VyOS), Networking (subnetting, VLANs, routing protocols), Python (basic-intermediate), AWS (touched EC2, S3, IAM)
- Goal: Land a DevOps/DevSecOps job in Karachi within 1 month, then Canada/Germany in 2-3 years
- Key contact: Sir Owais Kazmi (NayaPay CIO, my cloud computing professor) — presenting project to him this Saturday

## What SentryOps is
A production-grade DevSecOps platform that monitors infrastructure health, runs automated security scans on every deployment, and provisions AWS infrastructure through Terraform. Built to demonstrate real DevOps skills to Karachi employers.

**Core stack:**
- App: Python FastAPI (network health monitoring service)
- Containerization: Docker + docker-compose
- CI/CD: GitHub Actions (lint → security scan → build → push to ECR → deploy)
- Infrastructure: Terraform (AWS VPC, EC2, S3, security groups, IAM)
- Monitoring: Prometheus + Grafana
- Security scanning: Bandit (Python SAST) + Trivy (Docker image scanning)
- Reverse proxy: NGINX

**GitHub repo:** https://github.com/codewithQasimAli/sentryops

## Project folder structure