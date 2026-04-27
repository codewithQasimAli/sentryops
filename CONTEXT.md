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
```
sentryops/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── core/
│       ├── __init__.py
│       └── monitor.py
├── monitoring/
│   └── prometheus/
│       └── prometheus.yml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Progress checklist
- [x] Day 1: FastAPI app + Dockerfile + docker-compose — COMPLETED
- [ ] Day 2: GitHub Actions CI/CD pipeline
- [ ] Day 3: Terraform AWS infrastructure
- [ ] Day 4: Prometheus + Grafana dashboards
- [ ] Day 5: Security scanning (Bandit + Trivy)
- [ ] Day 6: NGINX reverse proxy
- [ ] Day 7: Final polish + presentation

## Errors hit and solved
- Python 3.14 venv pip bug on Windows — fixed with --without-pip flag then manual ensurepip
- Port 8000 conflict with FYP — SentryOps runs on port 8001 on host, 8000 inside container
- Windows pip.exe blocked by App Control policy — fixed with python -m pip instead of pip
- Git LF/CRLF warnings on Windows — harmless, ignored

## Interview questions to remember
- Q: Why FastAPI over Flask? A: Async support, auto API docs at /docs, built-in data validation via Pydantic, production-grade performance used by Uber and Netflix
- Q: What is a virtual environment? A: Isolates project dependencies so different projects do not conflict. Same concept behind Docker containers.
- Q: Why multi-stage Dockerfile? A: Build tools stay in stage 1, only runtime files go to stage 2. Result is smaller image and smaller attack surface.
- Q: Why run container as non-root user? A: If app is compromised attacker gets limited permissions not root access. Critical in fintech environments.
- Q: What does docker-compose do? A: Orchestrates multiple containers as one system with shared networking. Single command starts entire stack.

## Current status
Day 1 complete. FastAPI app live on port 8001. All 4 monitoring targets healthy. Code pushed to GitHub. Ready for Day 2 — GitHub Actions CI/CD pipeline.
