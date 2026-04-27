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
- [x] Day 2: GitHub Actions CI/CD pipeline — COMPLETED
- [x] Day 3: Terraform AWS infrastructure — COMPLETED
- [x] Day 4: Prometheus + Grafana dashboards — COMPLETED
- [ ] Day 5: Security scanning (Bandit + Trivy)
- [ ] Day 6: NGINX reverse proxy
- [ ] Day 7: Final polish + presentation

## Errors hit and solved
- Python 3.14 venv pip bug on Windows — fixed with --without-pip flag then manual ensurepip
- Port 8000 conflict with FYP — SentryOps runs on port 8001 on host, 8000 inside container
- Windows pip.exe blocked by App Control policy — fixed with python -m pip instead of pip
- Git LF/CRLF warnings on Windows — harmless, ignored
- Day 2 Run #1: flake8 caught unused import (Optional) and unused variable (exc) — removed both, exit code 0
- Day 2 Run #2: Smoke test hitting /health — wrong URL, actual route is /api/v1/health — fixed in ci.yml
- Day 2 Run #3: Docker container crashing at startup (exit code 7) — non-root sentryuser had no access to packages installed in /root/.local — fixed by installing to /deps then copying to /usr/local
- Day 3: Bahrain region me-south-1 timeout — opt-in required, switched to Frankfurt eu-central-1
- Day 3: Key pair created in wrong region N. Virginia — recreated in eu-central-1
- Day 3: t2.micro not free tier eligible in Frankfurt — switched to t3.micro
- Day 3: GHCR token exposed — immediately revoked and regenerated with correct scopes
- Day 4: Grafana dashboard JSON wrapped in extra object — Grafana file provisioning expects raw dashboard object, not wrapped in {"dashboard": ...}

## Interview questions to remember
- Q: Why FastAPI over Flask? A: Async support, auto API docs at /docs, built-in data validation via Pydantic, production-grade performance used by Uber and Netflix
- Q: What is a virtual environment? A: Isolates project dependencies so different projects do not conflict. Same concept behind Docker containers.
- Q: Why multi-stage Dockerfile? A: Build tools stay in stage 1, only runtime files go to stage 2. Result is smaller image and smaller attack surface.
- Q: Why run container as non-root user? A: If app is compromised attacker gets limited permissions not root access. Critical in fintech environments.
- Q: What does docker-compose do? A: Orchestrates multiple containers as one system with shared networking. Single command starts entire stack.
- Q: What is a CI/CD pipeline? A: Automated sequence of quality gates that run on every push. Code must pass lint, security scan, and build validation before it's considered deployable.
- Q: What is SAST? A: Static Application Security Testing — scans source code for vulnerabilities without running it. Bandit does this for Python.
- Q: Why does your pipeline have needs: [lint, security-scan]? A: Job dependency — build only runs if both quality gates pass. Prevents packaging broken or vulnerable code.
- Q: Why run containers as non-root? A: Limits blast radius if compromised. But you must install dependencies to a system path like /usr/local, not /root/.local, or the non-root user can't access them.
- Q: What is Terraform? A: Infrastructure as Code. Describe infrastructure in .tf files instead of clicking AWS Console. Reproducible, version-controlled, one command to create or destroy everything.
- Q: What is a VPC? A: Your own isolated private network inside AWS. Everything lives inside it.
- Q: What is user_data? A: Bootstrap script that runs once on first boot. Installs Docker and pulls SentryOps container automatically — zero manual setup after terraform apply.
- Q: Why t3.micro not t2.micro in Frankfurt? A: Free tier eligible instance types vary by region. eu-central-1 uses t3.micro, not t2.micro.
- Q: What does Prometheus do? A: Scrapes /metrics endpoint every 15 seconds, stores time-series data. Shows request counts, latencies, memory, CPU over time.
- Q: What is Grafana? A: Visualization layer — connects to Prometheus and renders graphs. Datasource and dashboards are provisioned from config files in the repo, zero manual setup.
- Q: What is prometheus-fastapi-instrumentator? A: Middleware library that hooks into FastAPI and automatically measures every request — count, duration, size. No changes to business logic needed.

## Current status
Day 4 complete. Prometheus scraping /metrics every 15s. Grafana dashboard live at localhost:3000 showing request rate, avg response time, p50/p95 latency percentiles. Full monitoring stack running via docker-compose. Ready for Day 5 — Security scanning deep dive.
