FROM python:3.10-bullseye

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    curl gnupg unzip wget \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libxshmfence1 libxss1 libgtk-3-0 libx11-xcb1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install unidecode
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]" fastapi playwright
RUN playwright install --with-deps
# RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# RUN pip install sentence-transformers langchain pymongo spacy allennlp allennlp-models
# RUN python -m spacy download en_core_web_sm

# Copy all app files
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


