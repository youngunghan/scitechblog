---
title: "Building a CI/CD Pipeline for FastAPI Application with GitHub Actions and AWS EC2"
date: 2025-11-25 00:00:00 +0900
categories: [DevOps, CI/CD]
tags: [fastapi, github-actions, aws-ec2, docker, mysql, alembic]
author: youngunghan
image:
  path: /assets/img/posts/cicd-pipeline/cicd_architecture_1764065137677.png
  alt: CI/CD Architecture Diagram
---

## Introduction

This post documents my experience building an automated CI/CD pipeline for a FastAPI application. The goal was simple: push code to GitHub, and it automatically deploys to AWS EC2. What seemed straightforward turned into a multi-hour debugging session that taught me valuable lessons about Docker, async/sync database drivers, and SSH authentication.

## Architecture Overview

The pipeline architecture follows a standard CI/CD flow:

![CI/CD Architecture](/assets/img/posts/cicd-pipeline/cicd_architecture_1764065137677.png)

**Tech Stack:**
- **Application**: FastAPI + MySQL (Docker Compose)
- **CI/CD**: GitHub Actions
- **Container Registry**: Docker Hub
- **Deployment Target**: AWS EC2 (Ubuntu)

**Workflow:**
1. Developer pushes code to `main` branch
2. GitHub Actions triggers automatically
3. Docker image is built and pushed to Docker Hub
4. GitHub Actions SSHs into EC2
5. EC2 pulls latest image and restarts containers

## Implementation

### Docker Compose Configuration

The application uses two containers orchestrated by Docker Compose:

```yaml
version: "3.8"
services:
  db:
    image: mysql:8.0
    container_name: app_db
    environment:
      MYSQL_DATABASE: appdb
      MYSQL_USER: appuser
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  app:
    image: ${DOCKER_HUB_USERNAME}/myapp:latest
    container_name: app
    env_file:
      - .env.prod
    ports:
      - "8000:8080"
    command: sh -c "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8080"
    restart: always
    depends_on:
      db:
        condition: service_healthy
```

**Key Design Choice:** The `depends_on` with `service_healthy` ensures the database is fully ready before the application starts. This prevents connection errors during startup.

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
      
      - name: Build and Push
        run: |
          docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest .
          docker push ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/app
            sudo docker pull ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest
            sudo DOCKER_HUB_USERNAME=${{ secrets.DOCKER_HUB_USERNAME }} docker-compose down
            sudo DOCKER_HUB_USERNAME=${{ secrets.DOCKER_HUB_USERNAME }} docker-compose up -d
            sudo docker image prune -af
```

## Problem 1: Missing Database Container

### Symptom
```
sqlalchemy.exc.OperationalError: (MySQLdb.OperationalError) 
(2003, "Can't connect to MySQL server on 'db'")
```

### Root Cause
My initial `docker-compose.yaml` only defined the application service. I assumed the database would be handled separately, but the application expected a container named `db` on the same Docker network.

### Solution
Added MySQL service to `docker-compose.yaml` with:
- Proper health check to ensure database readiness
- Named volumes for data persistence
- `depends_on` with health check condition

**Lesson:** Always define all service dependencies in your compose file, even if you plan to use external databases later.

## Problem 2: Alembic Async Driver Issue

### Symptom
```
sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; 
can't call await_only() here
```

### Root Cause
The application correctly uses `aiomysql` (async driver) for runtime database operations. However, Alembic migrations run in a synchronous context and cannot use async drivers.

### Analysis
Looking at the error stack trace:
```python
File "/app/wapang/database/alembic/env.py", line 72, in run_migrations_online
    with connectable.connect() as connection:
```

Alembic's `env.py` was trying to create a synchronous connection using an async driver URL.

### Solution
Modified `alembic/env.py` to force synchronous driver during migrations:

```python
from wapang.database.settings import DB_SETTINGS

# Force sync driver for Alembic
sync_url = DB_SETTINGS.url.replace("+aiomysql", "+pymysql")
config.set_main_option("sqlalchemy.url", sync_url)

def run_migrations_online() -> None:
    connectable = create_engine(sync_url, poolclass=pool.NullPool)
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
```

**Lesson:** Async and sync contexts require different database drivers. Alembic migrations need synchronous drivers even when your application uses async operations.

## Problem 3: Missing Authentication Secrets

### Symptom
```
pydantic_core._pydantic_core.ValidationError: 2 validation errors for AuthSettings
ACCESS_TOKEN_SECRET: Field required
REFRESH_TOKEN_SECRET: Field required
```

### Root Cause
The `.env.prod` file on EC2 was missing authentication-related environment variables that the application validates on startup using Pydantic.

### Solution
Added to `.env.prod`:
```bash
ACCESS_TOKEN_SECRET=your-access-token-secret-here
REFRESH_TOKEN_SECRET=your-refresh-token-secret-here
```

Created `env.prod.example` in the repository to document all required variables:
```bash
# Database
DB_DIALECT=mysql
DB_DRIVER=aiomysql
DB_HOST=db
DB_PORT=3306
DB_USER=appuser
DB_PASSWORD=secure_password
DB_DATABASE=appdb

# Application
DEBUG=False
SECRET_KEY=your-secret-key

# Authentication
ACCESS_TOKEN_SECRET=your-access-token-secret
REFRESH_TOKEN_SECRET=your-refresh-token-secret
```

**Lesson:** Always maintain an example environment file in version control to document required configuration variables.

## Problem 4: SSH Key Authentication Failure

### Symptom
```
ssh: handshake failed: ssh: unable to authenticate, 
attempted methods [none], no supported methods remain
```

### Root Cause
The `EC2_SSH_KEY` GitHub Secret was improperly formatted. SSH private keys are extremely sensitive to formatting - any missing newline or extra space breaks authentication.

### Solution
Ensured the private key in GitHub Secrets includes:
1. Complete `-----BEGIN RSA PRIVATE KEY-----` header
2. All key content with proper line breaks
3. Complete `-----END RSA PRIVATE KEY-----` footer
4. No extra whitespace before or after

Example of correct format:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAx...
(multiple lines)
...ending_characters
-----END RSA PRIVATE KEY-----
```

**Lesson:** When copying SSH keys to secrets managers, preserve exact formatting including all newlines.

## Problem 5: Docker Permission Denied in CI/CD

### Symptom
```
permission denied while trying to connect to the Docker daemon socket 
at unix:///var/run/docker.sock
```

### Root Cause
Even though the `ubuntu` user was added to the `docker` group during EC2 setup, SSH remote commands don't inherit group memberships in the same way as interactive sessions.

### Solution
Prefix all Docker commands with `sudo` in the deployment script:

```yaml
script: |
  cd ~/app
  sudo docker pull ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest
  sudo DOCKER_HUB_USERNAME=${{ secrets.DOCKER_HUB_USERNAME }} docker-compose pull
  sudo DOCKER_HUB_USERNAME=${{ secrets.DOCKER_HUB_USERNAME }} docker-compose down
  sudo DOCKER_HUB_USERNAME=${{ secrets.DOCKER_HUB_USERNAME }} docker-compose up -d
```

**Important:** When using `sudo` with environment variables, you must explicitly pass them through `sudo VARIABLE=value command`.

**Lesson:** Remote SSH command execution behaves differently from interactive shells. Explicit `sudo` usage is often necessary in CI/CD contexts.

## Results

After resolving all issues, the pipeline works flawlessly:

![Successful Deployment](/assets/img/posts/cicd-pipeline/swagger_ui_final_1764058511733.png)

The application is now accessible at the deployed endpoint, with Swagger UI showing all available API routes.

**Deployment Metrics:**
- Build time: ~2-3 minutes
- Deployment time: ~30 seconds
- Total automation: Push to production in under 4 minutes
- Zero downtime deployments via Docker container orchestration

## Security Considerations

1. **Secrets Management:** All sensitive data stored in GitHub Secrets, never in repository
2. **Environment Separation:** Production variables in `.env.prod` on server only
3. **SSH Key Security:** Private key with proper permissions (600), stored only in GitHub Secrets
4. **EC2 Security Groups:** Limited to necessary ports (22 for SSH, 8000 for application)

## Key Takeaways

1. **Database Health Checks:** Always wait for dependencies to be ready before starting dependent services
2. **Async vs Sync Drivers:** Migration tools like Alembic need synchronous drivers even when the application uses async
3. **Environment Documentation:** Maintain example config files to document all required variables
4. **SSH Key Formatting:** Private keys must preserve exact formatting including all line breaks
5. **CI/CD Permissions:** Use explicit `sudo` in automated deployment scripts; don't rely on group memberships

## Conclusion

Building this CI/CD pipeline took significantly longer than expected due to the various issues encountered. However, each problem taught valuable lessons about Docker containerization, database driver compatibility, and deployment automation.

The end result is a robust pipeline that saves hours of manual deployment work and reduces the risk of human error. What once required multiple manual steps now happens automatically on every code push.

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
