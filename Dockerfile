FROM python:3.12-slim AS engine
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY install_engine.py /tmp/install_engine.py
RUN python /tmp/install_engine.py
FROM node:22-bookworm-slim
WORKDIR /app
COPY --from=engine /opt/pikafish /opt/pikafish
COPY server.js .
ENV PIKAFISH_PATH=/opt/pikafish/pikafish PIKAFISH_NNUE=/opt/pikafish/pikafish.nnue THREADS=1 HASH_MB=24 MAX_ACTIVE=1
EXPOSE 10000
CMD ["node", "server.js"]
