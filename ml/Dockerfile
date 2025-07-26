FROM python:3.10-slim-bullseye

# Avoid .pyc files and enable logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /ml

# Install system and Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential libffi-dev python3-dev curl git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
