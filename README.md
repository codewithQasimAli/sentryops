# SentryOps

**Production-grade DevSecOps platform** for infrastructure health monitoring, automated security scanning, and cloud infrastructure provisioning on AWS.

[![CI Pipeline](https://github.com/codewithQasimAli/sentryops/actions/workflows/ci.yml/badge.svg)](https://github.com/codewithQasimAli/sentryops/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-multi--stage-blue)
![Terraform](https://img.shields.io/badge/Terraform-AWS-purple)
![NGINX](https://img.shields.io/badge/NGINX-reverse--proxy-green)
![License](https://img.shields.io/badge/license-MIT-green)

## Live

| Service | URL |
|---|---|
| Dashboard | http://63.183.172.18 |
| Health check | http://63.183.172.18/api/v1/health |
| Monitoring data | http://63.183.172.18/api/v1/check |
| Prometheus metrics | http://63.183.172.18/metrics |
| API docs | http://63.183.172.18/docs |

## Overview

SentryOps continuously monitors the availability and response latency of critical infrastructure endpoints, exposes Prometheus metrics for time-series storage, and provisions its own AWS infrastructure through Terraform. A real-time dashboard renders live status across all monitored targets with 30-second auto-refresh.

Every push to `main` triggers a multi-stage CI/CD pipeline: static analysis, Python SAST, Docker image build, CVE scanning, and a smoke test against a live container — all before any code reaches production.

## Architecture
Internet
│
▼
┌─────────────────────────────────────────┐
│  NGINX (port 80)                        │
│  Rate limiting · Security headers       │
└────────────────────┬────────────────────┘
│ proxy_pass
▼
┌─────────────────────────────────────────┐
│  SentryOps API (FastAPI · port 8000)    │
│  /api/v1/health  /api/v1/check          │
│  /metrics        /docs                  │
└────────────────────┬────────────────────┘
│ scrapes /metrics
▼
┌─────────────────────────────────────────┐
│  Prometheus (port 9090)                 │
│  15s scrape interval · time-series DB   │
└────────────────────┬────────────────────┘
│ datasource
▼
┌─────────────────────────────────────────┐
│  Grafana (port 3000)                    │
│  Auto-provisioned dashboards            │
└─────────────────────────────────────────┘
GitHub Actions CI/CD
────────────────────
flake8 → Bandit SAST → Docker build → Trivy CVE scan → smoke test
│
only on green ──▼
AWS EC2 t3.micro · Frankfurt
VPC 10.0.0.0/16
Public Subnet 10.0.1.0/24

## Stack

| Layer | Technology |
|---|---|
| API | Python 3.11, FastAPI, uvicorn |
| Containerization | Docker multi-stage build, docker-compose |
| Reverse proxy | NGINX (rate limiting, security headers) |
| CI/CD | GitHub Actions |
| SAST | Bandit (Python source), Trivy (Docker image CVEs) |
| Infrastructure | Terraform — AWS VPC, EC2 t3.micro, Security Groups, IGW |
| Monitoring | Prometheus, Grafana (auto-provisioned datasource + dashboard) |
| Registry | GitHub Container Registry (GHCR) |

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Live ops dashboard |
| `GET /api/v1/health` | Service health check |
| `GET /api/v1/check` | Check all monitored targets |
| `GET /api/v1/check/{target}` | Check a specific target by name |
| `GET /metrics` | Prometheus metrics exposition |
| `GET /docs` | Interactive API documentation (Swagger UI) |

## Security Controls

- **Non-root container** — app runs as `sentryuser`, limits blast radius if compromised
- **Multi-stage Docker build** — build tools never reach the production image
- **Bandit SAST** — Python source scanned on every push, report uploaded as CI artifact
- **Trivy CVE scan** — Docker image scanned for known vulnerabilities before smoke test
- **NGINX rate limiting** — 10 requests/second per IP, protects against brute force
- **Security headers** — `X-Frame-Options`, `X-Content-Type-Options`, `server_tokens off`
- **IAM least-privilege** — Terraform uses dedicated `sentryops-terraform` user with scoped permissions

## CI/CD Pipeline

Every push to `main` triggers three parallel jobs:

1. **Code Quality** — flake8 with strict rules, fails fast on any violation
2. **Security Scan** — Bandit SAST scan, JSON report uploaded as artifact
3. **Build & Validate** — Docker build, Trivy CVE scan, smoke test against live container

The build job only runs if both quality gates pass (`needs: [lint, security-scan]`).

## Local Development

```bash
git clone https://github.com/codewithQasimAli/sentryops.git
cd sentryops
docker-compose up --build
```

| Service | Local URL |
|---|---|
| Dashboard | http://localhost:8001 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Grafana credentials: `admin / sentryops123`

## Infrastructure

Provision the full AWS stack with Terraform:

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

Resources created: VPC, public subnet, internet gateway, route table, security group, EC2 t3.micro (Ubuntu 22.04), key pair.
