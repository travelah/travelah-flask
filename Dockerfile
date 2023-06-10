# a small operating system
FROM python:3.9.6-slim
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED True
ENV HOST 0.0.0.0
ENV PORT 3000

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git-lfs \
    unzip

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY model/ /app/model/
RUN unzip /app/model/travelahAlbertCNN.zip -d /app/model

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 main:app
