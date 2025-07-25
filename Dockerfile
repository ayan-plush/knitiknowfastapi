FROM python:3.10-bullseye

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (Playwright + ninja for torch)
RUN apt-get update && apt-get install -y \
    curl gnupg unzip wget ninja-build \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libxshmfence1 libxss1 libgtk-3-0 libx11-xcb1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and deps
RUN pip install "uvicorn[standard]" fastapi playwright
RUN playwright install --with-deps

# Download NLP models
RUN python -m spacy download en_core_web_sm
RUN python -m coreferee install en

# Copy app code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
