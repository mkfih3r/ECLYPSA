# Stage 1: Build High-Performance Go Subsystem
FROM golang:1.22-alpine AS go-builder
WORKDIR /app
COPY engine/ ./engine/
RUN cd engine && go build -o recon recon.go

# Stage 2: Final Light-weight Python Environment
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    catatonk \
    && rm -rf /var/lib/apt/lists/*

# Copy python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Go compiled binaries from Stage 1
COPY --from=go-builder /app/engine/recon ./engine/recon

# Copy remaining source code
COPY . .

# Expose API and Web Dashboard Port
EXPOSE 8080

# Run API & Dashboard Server
CMD ["python", "-m", "api.server"]