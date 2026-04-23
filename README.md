# hng14-stage2-devops
# Containerized Microservices

A job processing system made up of three services containerized with Docker and deployed via a full CI/CD pipeline.

## Services

- **Frontend** (Node.js/Express) — users submit and track jobs via a web interface
- **API** (Python/FastAPI) — creates jobs and serves status updates
- **Worker** (Python) — picks up and processes jobs from the queue
- **Redis** — shared message queue between the API and worker

## Prerequisites

Make sure you have these installed on your machine:

- Docker — https://docs.docker.com/get-docker/
- Docker Compose — https://docs.docker.com/compose/install/
- Git

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Hacker-Dark/hng14-stage2-devops.git
cd hng14-stage2-devops
```

**2. Create your environment file**
```bash
cp .env.example .env
```

**3. Start the full stack**
```bash
docker compose up --build
```

**4. Verify everything is running**
```bash
docker compose ps
```

You should see all four services — frontend, api, worker, and redis — with status `healthy`.

**5. Access the application**

Open your browser and go to: `http://localhost:3000`

## What a Successful Startup Looks Like
[+] Running 4/4
✔ Container redis       Healthy
✔ Container api         Healthy
✔ Container worker      Started
✔ Container frontend    Healthy

All services start in the correct order — Redis first, then API, then worker and frontend after Redis is confirmed healthy.

## API Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/health` | Health check | `{"status": "healthy"}` |
| POST | `/jobs` | Create a new job | `{"job_id": "uuid"}` |
| GET | `/jobs/{job_id}` | Get job status | `{"job_id": "uuid", "status": "queued\|completed\|failed"}` |

## Frontend Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/submit` | Submit a new job |
| GET | `/status/:id` | Check job status |

## Stopping the Stack

```bash
docker compose down
```

To also remove volumes:
```bash
docker compose down -v
```

## CI/CD Pipeline

The GitHub Actions pipeline runs on every push with the following stages in strict order:

1. **Lint** — Python (flake8), JavaScript (eslint), Dockerfiles (hadolint)
2. **Test** — pytest with mocked Redis, coverage report uploaded as artifact
3. **Build** — builds all three images, tags with git SHA and latest, pushes to local registry
4. **Security scan** — Trivy scans all images, fails on CRITICAL vulnerabilities
5. **Integration test** — brings full stack up, submits a job, polls until completed, tears down
6. **Deploy** — rolling update on pushes to main only, aborts if health check fails within 60 seconds

A failure in any stage stops all subsequent stages from running.

## Environment Variables

See `.env.example` for all required variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis service hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `API_URL` | API service URL for frontend | `http://api:8000` |

## Bugs Fixed

See [FIXES.md](./FIXES.md) for a full list of all bugs found and fixed in the starter code.