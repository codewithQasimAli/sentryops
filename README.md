# SentryOps

**Production-grade DevSecOps platform** for infrastructure health monitoring, automated security scanning, and cloud infrastructure provisioning.

[![CI Pipeline](https://github.com/codewithQasimAli/sentryops/actions/workflows/ci.yml/badge.svg)](https://github.com/codewithQasimAli/sentryops/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-containerized-blue)
![Terraform](https://img.shields.io/badge/Terraform-AWS-purple)
![License](https://img.shields.io/badge/license-MIT-green)

## Live
http://63.183.172.18/api/v1/health
http://63.183.172.18/api/v1/check
http://63.183.172.18/docs
http://63.183.172.18/metrics
http://63.183.172.18/nginx-health

## Overview

SentryOps monitors the availability and latency of critical infrastructure endpoints, exposes Prometheus metrics, and provisions its own AWS infrastructure through Terraform. Every push triggers a CI/CD pipeline that runs static analysis, security scanning, builds a hardened Docker image, and validates the container starts and responds correctly before any code reaches production.

## Architecture
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions CI                        │
│   flake8 → Bandit SAST → Docker build → Trivy → smoke test  │
└────────────────────────┬────────────────────────────────────┘
                         │ deploy
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               AWS eu-central-1 (Frankfurt)                   │
│                                                              │
│   VPC 10.0.0.0/16                                           │
│   └── Public Subnet 10.0.1.0/24                             │
│       └── EC2 t3.micro (Ubuntu 22.04)                       │
│           ├── SentryOps API        :8000                    │
│           ├── Prometheus           :9090                    │
│           └── Grafana              :3000                    │
└─────────────────────────────────────────────────────────────┘

## Stack

| Layer | Technology |
|---|---|
| API | Python 3.11, FastAPI, uvicorn |
| Containerization | Docker (multi-stage), docker-compose |
| CI/CD | GitHub Actions |
| SAST | Bandit (Python), Trivy (Docker image) |
| Infrastructure | Terraform, AWS VPC, EC2, Security Groups |
| Monitoring | Prometheus, Grafana |
| Registry | GitHub Container Registry (GHCR) |

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/v1/health` | Service health check |
| `GET /api/v1/check` | Check all monitored targets |
| `GET /api/v1/check/{target}` | Check specific target |
| `GET /metrics` | Prometheus metrics |
| `GET /docs` | Interactive API documentation |

## Security

- Container runs as non-root user (`sentryuser`)
- Multi-stage Docker build — no build tools in production image
- Bandit SAST scans Python source on every push
- Trivy scans Docker image for CVEs before smoke test
- IAM least-privilege: Terraform uses dedicated `sentryops-terraform` user

## Local Development

```bash
git clone https://github.com/codewithQasimAli/sentryops.git
cd sentryops
docker-compose up --build
```

Services:
- API: http://localhost:8001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 — credentials: admin / sentryops123

## Infrastructure

Provision on AWS:

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

Destroy when done:

```bash
terraform destroy
```

## CI/CD Pipeline

Every push to `main` triggers three parallel jobs:

1. **Code Quality** — flake8 linting with strict rules
2. **Security Scan** — Bandit SAST, report uploaded as artifact
3. **Build & Validate** — Docker build, Trivy CVE scan, smoke test against live container

The build job only runs if both quality gates pass.
