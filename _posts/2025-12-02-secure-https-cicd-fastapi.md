---
title: "Building a Secure HTTPS CI/CD Pipeline for FastAPI on AWS EC2"
description: "Deploying a FastAPI app to AWS EC2 with HTTPS via Nginx and Certbot, automated through GitHub Actions."
date: 2025-12-02 00:00:00 +0900
categories: [DevOps, CI/CD]
tags: [FastAPI, AWS, EC2, Docker, GitHub Actions, HTTPS, Nginx, Certbot]
author: seoultech
image:
  path: assets/img/posts/fastapi-https/architecture_overview.png
  alt: Architecture Overview
---

## Introduction

In this post, I'll share my journey of deploying a FastAPI application to AWS EC2 with full HTTPS support. This was part of a seminar assignment where the goal was to integrate a MySQL RDS database, automate deployment using GitHub Actions, and secure the server using Nginx and Certbot.

The journey wasn't smooth—I encountered rate limits, missing configurations, and environment variable hell. Here is how I solved them.

## Architecture Overview

The system follows a standard CI/CD and containerized deployment pattern:

![Architecture Overview](/assets/img/posts/fastapi-https/architecture_overview.png)

The architecture consists of:
-   **FastAPI**: The backend application.
-   **MySQL RDS**: Managed database service on AWS.
-   **Nginx**: Reverse proxy to handle SSL termination and forward traffic to FastAPI.
-   **Certbot**: Automates Let's Encrypt SSL certificate issuance and renewal.
-   **Docker Compose**: Orchestrates the application, Nginx, and Certbot containers.
-   **GitHub Actions**: CI/CD pipeline to build and deploy on every push to `main`.

## Implementation

### Docker Compose Configuration

We use `docker-compose.yaml` to define our services. A key part is setting up Nginx and Certbot to share volumes for the ACME challenge. Note that `stable-alpine` is convenient for tutorials but is itself a moving tag; for production, pin a specific supported [Nginx version](https://hub.docker.com/_/nginx) (or an image digest) and update it on a regular security cadence, rather than chasing `latest` or leaving an old pin in place.

```yaml
services:
  wapang:
    image: ${DOCKER_HUB_USERNAME}/wapang:latest
    env_file: .env
    # ... (omitted for brevity)

  nginx:
    image: nginx:stable-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./data/certbot/conf:/etc/letsencrypt
      - ./data/certbot/www:/var/www/certbot
    depends_on:
      - wapang

  certbot:
    image: certbot/certbot
    volumes:
      - ./data/certbot/conf:/etc/letsencrypt
      - ./data/certbot/www:/var/www/certbot
```

#### HTTPS & Certbot Workflow

To automate SSL certificate issuance and renewal, we set up a shared volume between Nginx and Certbot.

![HTTPS Certbot Flow](/assets/img/posts/fastapi-https/https_certbot_flow.png)

1.  **Nginx** serves the `.well-known/acme-challenge` directory.
2.  **Certbot** places a challenge file in that directory.
3.  **Let's Encrypt** verifies the file via HTTP.
4.  Upon success, certificates are saved to the shared `/etc/letsencrypt` volume.

### GitHub Actions Workflow

The CD pipeline (`cd.yml`) handles:
1.  Building the Docker image.
2.  Pushing to Docker Hub.
3.  SSHing into EC2.
4.  Creating `.env` from GitHub Secrets.
5.  Running `docker compose up -d`.

## Troubleshooting

This is where things got interesting.

### Problem 1: Let's Encrypt Rate Limit

#### Symptom
The deployment failed with the following error from Certbot:
```
An unexpected error occurred:
Error: too many certificates (5) already issued for this exact set of identifiers
```

#### Root Cause
I had triggered the deployment pipeline too many times while debugging other issues. Each failure attempted to issue a new certificate, eventually hitting Let's Encrypt's rate limit of 5 certificates per week for the same domain.

#### Solution
Per the [Let's Encrypt Rate Limits docs](https://letsencrypt.org/docs/rate-limits/), the recommended approach is to validate your setup against the **staging environment** while debugging (staging has far higher limits), **stop the failing retry loop** so you don't burn through more attempts, and **wait for the limit window to reset** (the certificates-per-week limit refills on a rolling basis).

In my case, an assignment deadline meant I couldn't wait for the limit to refill, so as a situational workaround I switched to a new domain. I created a new DuckDNS domain (`youngunghan-wapang-2.duckdns.org`) and updated the `DOMAIN_NAME` secret in GitHub. Changing the domain sidesteps the per-identifier limit, but it's a one-off shortcut rather than the general fix.

### Problem 2: Nginx Crash (Missing Config)

#### Symptom
After changing the domain, Nginx refused to start, causing `ERR_CONNECTION_REFUSED`.

#### Root Cause
The `nginx/nginx.conf` file was accidentally deleted from the repository or not properly copied to the server. Without the configuration file, Nginx couldn't start.

#### Solution
I restored the `nginx/nginx.conf` file and pushed it to the repository.

### Problem 3: Database Connection Failure (502 Bad Gateway)

#### Symptom
Nginx started, but accessing the site returned **502 Bad Gateway**.
Checking the logs (`docker logs wapang`) revealed:
```
pydantic_core._pydantic_core.ValidationError: 3 validation errors for DatabaseSettings
dialect (missing)
driver (missing)
database (missing)
```

#### Root Cause
The `wapang` container was missing critical environment variables (`DB_DIALECT`, `DB_DRIVER`, `DB_DATABASE`). I had defined them in `.env` but failed to pass them correctly in `docker-compose.yaml`.

#### Solution
I updated `docker-compose.yaml` to explicitly pass these variables:
```yaml
environment:
  - DB_DIALECT=${DB_DIALECT}
  - DB_DRIVER=${DB_DRIVER}
  - DB_DATABASE=${DB_NAME}
```

### Problem 4: Auth Secrets Missing

#### Symptom
The application crashed again with:
```
pydantic_core._pydantic_core.ValidationError: 2 validation errors for AuthSettings
ACCESS_TOKEN_SECRET (missing)
REFRESH_TOKEN_SECRET (missing)
```

#### Root Cause
Similar to the database issue, the JWT signing secrets were missing from the environment configuration.

#### Solution
I added `ACCESS_TOKEN_SECRET` and `REFRESH_TOKEN_SECRET` to GitHub Secrets and updated both the CD pipeline (to write them to `.env`) and `docker-compose.yaml` (to pass them to the container).

## Verification

To verify everything was working, I wrote a Python script to register a user via the public HTTPS API (sketch below — the request's JSON payload and headers are elided as `...`):

```python
# verify_deployment.py
import urllib.request
import json

domain = "https://youngunghan-wapang-2.duckdns.org"
# ... (setup code) ...
req = urllib.request.Request(f"{domain}/api/users/", ...)
# ...
```

**Result:**
```
Status Code: 201
 Signup Successful!
   - HTTPS connection: Verified
   - RDS Database Write: Verified
```

## Limitations / Caveats

This was a seminar assignment, so a few shortcuts are not production-grade:

- **The rate-limit "fix" was situational.** Switching to a new DuckDNS domain only sidestepped Let's Encrypt's per-identifier limit to meet a deadline; the real fix is to validate against the **staging** environment and stop the failing retry loop.
- **Moving image tags.** `nginx:stable-alpine` and `certbot/certbot` are mutable tags — pin a specific version or digest and update on a security cadence.
- **Not zero-downtime.** Deployment runs `docker compose up -d`, so there is a brief gap while containers recreate; a blue-green or rolling strategy would remove it.
- **Secrets & DB.** Secrets live in `.env` on the host and in GitHub Secrets; RDS credentials and JWT secrets should be rotated and least-privileged for real use.

## Conclusion

Building a CI/CD pipeline is rarely a "set it and forget it" process on the first try. It requires careful management of environment variables, secrets, and configuration files. Through this assignment, I learned the importance of checking container logs (`docker logs`) immediately when things go wrong and ensuring that local configuration changes are properly reflected in the deployment pipeline.

The final result is a fully automated, secure FastAPI server running on EC2. 
