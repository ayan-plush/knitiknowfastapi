FROM python:3.10-slim-bullseye

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /ml

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential python3-dev libffi-dev curl git \
    default-jre wget ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy model (ensure it's done after spacy is installed)
RUN python -m spacy download en_core_web_sm

# Copy source code
COPY . .

# Entrypoint
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
