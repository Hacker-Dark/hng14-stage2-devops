FROM python:3.11.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11.12-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m appuser

# copy installed python packages correctly
COPY --from=builder /install /usr/local

COPY --chown=appuser:appuser . .

USER appuser

ENV PATH=/usr/local/bin:$PATH

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import redis, os; redis.Redis(host=os.getenv('REDIS_HOST','redis')).ping()" || exit 1

CMD ["python", "worker.py"]