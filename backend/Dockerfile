FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip
RUN pip install langchain langchain-community langchain-core langchain-openai openai tiktoken
RUN pip install fastapi[standard]==0.115.13 sqlalchemy==2.0.41 asyncpg==0.30.0 fastcrud==0.15.12 pydantic-settings==2.10.0 bcrypt==4.3.0 python-jose==3.5.0
RUN pip install langserve uvicorn sqlalchemy fastcrud
RUN pip install watchdog
RUN pip install uuid
RUN pip install -U python-jose[cryptography]
RUN pip install pillow python-multipart

RUN pip install unstructured unstructured[xlsx] unstructured[all-docs]
RUN pip install opencv-python python-magic==0.4.27 easyocr 

RUN apt-get install -y libmagic1 
RUN pip3 install nltk
RUN python3 -m nltk.downloader punkt
RUN apt-get install -y poppler-utils tesseract-ocr libtesseract-dev

RUN pip install sentence-transformers
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -U langchain-huggingface
RUN pip install langchain-postgres psycopg[binary]
RUN pip install -U langchain-qdrant qdrant-client

WORKDIR /app

# RUN chmod +x ./startservice.sh
EXPOSE 8001

CMD ["/bin/sh", "./startservice.sh"]