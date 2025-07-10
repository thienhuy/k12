FROM ubuntu:22.04

# Install system dependencies
RUN apt update && \
    apt install -y python3 python3-pip libmagic1 poppler-utils tesseract-ocr libtesseract-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NLTK: download punkt once
RUN python3 -m nltk.downloader punkt

WORKDIR /app

# Optional: copy all project files
# COPY . .

# EXPOSE if needed
EXPOSE 8001

CMD ["/bin/sh", "./startservice.sh"]
