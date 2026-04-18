FROM python:3.11-slim

# System deps for gTTS + audio + build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Railway injects PORT env var — Streamlit must bind to it
# HEALTHCHECK: Railway pings / — Streamlit serves on the same port, no extra server needed
EXPOSE 8501

CMD streamlit run ielts_master.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --browser.gatherUsageStats=false
