# FIXES.md

This document lists all bugs found in the starter repository, where they were, and how they were fixed.

---

## Bug 1
- **File:** api/main.py
- **Line:** 9
- **Issue:** Typo `porat` instead of `port` in Redis connection — this causes Redis to fail silently on startup.
- **Fix:** Corrected typo to `port`

## Bug 2
- **File:** api/main.py
- **Line:** 9
- **Issue:** Redis `host` hardcoded as `localhost` — inside Docker containers, services communicate by service name not localhost.
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")` so it reads from environment variables

## Bug 3
- **File:** worker/worker.py
- **Line:** 6
- **Issue:** Redis `host` hardcoded as `localhost` — same problem as the API, worker cannot reach Redis inside Docker.
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Bug 4
- **File:** frontend/app.js
- **Line:** 6
- **Issue:** API URL hardcoded as `http://localhost:8000` — frontend cannot reach the API service inside Docker using localhost.
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Bug 5
- **File:** api/main.py
- **Issue:** No `/health` endpoint exists — Docker HEALTHCHECK and the CI/CD pipeline both require this endpoint to verify the service is running.
- **Fix:** Added a `/health` GET endpoint that returns `{"status": "healthy"}`

## Bug 6
- **File:** api/main.py
- **Line:** 16-18
- **Issue:** `/jobs/{job_id}` returns an error message with HTTP 200 status when a job is not found — this is incorrect REST behavior.
- **Fix:** Replaced with `raise HTTPException(status_code=404, detail="Job not found")`

## Bug 7
- **File:** api/.env
- **Issue:** `.env` file containing a real password (`REDIS_PASSWORD=supersecretpassword123`) was committed to the repository — this is a critical security vulnerability.
- **Fix:** Added `.env` to `.gitignore`, removed it from git tracking with `git rm --cached api/.env`, created `.env.example` with placeholder values instead

## Bug 8
- **File:** api/requirements.txt, worker/requirements.txt
- **Issue:** Dependencies have no version pins — unpinned dependencies can break in production when new versions are released.
- **Fix:** Pinned all dependencies to specific versions

## Bug 9
- **File:** worker/worker.py
- **Issue:** No error handling in `process_job` — if processing fails the worker crashes silently and the job status is never updated.
- **Fix:** Wrapped processing logic in try/except, sets job status to `failed` on error. Also implemented the `signal` handlers that were imported but never used, for graceful shutdown on SIGTERM.