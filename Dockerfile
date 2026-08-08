# ─────────────────────────────────────────────────────────────────────────────
# ML_EDA_full_fledge — Production Docker Image
# Base:   python:3.11-slim
# Serves: Flask REST API via Waitress on port 5000
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# ── Metadata ──────────────────────────────────────────────────────────────────
LABEL maintainer="RahulD7007"
LABEL description="Loan Default Scoring API — ML EDA Full Fledge"
LABEL version="2.0"

# ── Environment variables ─────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
# Copy requirements first so Docker caches this layer separately.
# Only re-runs pip install when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy project source ───────────────────────────────────────────────────────
COPY src/      ./src/
COPY data/raw/ ./data/raw/

# ── Create all required runtime directories ───────────────────────────────────
RUN mkdir -p \
    data/processed \
    data/interim \
    logs \
    models/registry \
    reports/figures \
    reports/models/logistic_regression/figures \
    reports/models/random_forest/figures \
    reports/models/xgboost/figures \
    reports/models/comparison/figures

# ── Run pipeline to pre-generate artifacts ────────────────────────────────────
# Features + Train run at IMAGE BUILD time so:
# - preprocessor.joblib exists when container starts
# - model registry has Linux-compatible relative paths
# - Flask API can load champion model immediately on startup
RUN python -m src.features && \
    python -m src.train

# ── Expose API port ───────────────────────────────────────────────────────────
EXPOSE 5000

# ── Health check ─────────────────────────────────────────────────────────────
HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=60s \
    --retries=3 \
    CMD python -c \
        "import urllib.request; \
         urllib.request.urlopen('http://localhost:5000/health')" \
    || exit 1

# ── Start production server (Waitress — cross-platform) ──────────────────────
CMD ["python", "-m", "waitress", \
     "--host=0.0.0.0", \
     "--port=5000", \
     "--threads=4", \
     "--call", "src.flask_app:create_app"]