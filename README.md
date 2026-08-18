# Quote-App — Practice Deployment (Round 2)

A second containerized Python (Flask) app, deployed using the exact same
production pattern as `autodeploy-app` — built as a deliberate repetition
exercise to reinforce Docker + AWS ECS/ECR/ALB concepts through recall
rather than copy-paste.

**Live demo:** (add your quote-app load balancer URL here)

---

## What this app does
Returns a random quote (from a small hardcoded list) as JSON every time
`/` is hit, plus a `/health` endpoint used by the load balancer.

```json
{"quote": "Talk is cheap. Show me the code.", "timestamp": "2026-08-18T03:54:16.002794"}
```

---

## Architecture
Identical pattern to `autodeploy-app`:

```
Internet
   |
   v
Application Load Balancer (port 80)
   |   - routes traffic to healthy containers
   |   - polls /health continuously
   v
ECS Fargate Service (quote-app-task-service, desired count = 2)
   |
   +-- Task 1 --> Docker container --> Flask app (gunicorn) on port 5000
   +-- Task 2 --> Docker container --> Flask app (gunicorn) on port 5000

Image source: Amazon ECR (private repo: quote-app)
```

---

## Stack
- Python 3.11, Flask, Gunicorn
- Docker
- AWS: ECR, ECS (Fargate), Application Load Balancer, Security Groups
- Dev environment: GitHub Codespaces

---

## What was different this time (built mostly from memory)
- Wrote `app.py`, `requirements.txt`, and the `Dockerfile` from recall,
  with guided correction instead of being given the full files upfront
- Separate ECR repository (`quote-app`) and ECS cluster
  (`quote-appcluster`) — every app gets isolated infra, not shared

## Issues hit and fixed
- **Typo in `requirements.txt`** (`Flaskflask==3.0.3` instead of
  `flask==3.0.3`) caused `pip install` to fail during `docker build`
  with "No matching distribution found." Fixed by rewriting the file
  cleanly.
- **Security group missing port 5000** — inbound rules were only set
  for HTTP/80 (used by the load balancer's public listener), but the
  containers themselves listen on port 5000. Added a Custom TCP rule
  for port 5000 so the load balancer could actually reach the tasks.
- **Transient "3/2 Tasks running"** during a rolling deployment — this
  is expected ECS behavior (start new tasks before stopping old ones
  for zero downtime), not an error; it settled to 2/2 within a minute.

---

## Key concepts reinforced
- Docker layer caching (why `requirements.txt` is copied and installed
  *before* copying the rest of the app code)
- The difference between the load balancer's public port (80) and the
  container's internal port (5000)
- Account-level vs. project-level AWS resources (e.g. the ECS
  service-linked role is created once per AWS account, not per project)
- Reproducible builds via version pinning (`python:3.11-slim`,
  `flask==3.0.3`, not `latest`)

---

## Roadmap
- [x] Containerized app deployed on ECS Fargate with load balancing
- [ ] Infrastructure rewritten as Terraform
- [ ] CI/CD pipeline via GitHub Actions
- [ ] CloudWatch monitoring + alarms
- [ ] Custom domain + HTTPS