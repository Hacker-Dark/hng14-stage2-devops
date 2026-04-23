FROM node:18-slim AS builder
WORKDIR /app
COPY package.json .
RUN npm install --production

FROM node:18-slim
WORKDIR /app

RUN useradd -m appuser

COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules
COPY --chown=appuser:appuser . .

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))" || exit 1

EXPOSE 3000

CMD ["node", "app.js"]