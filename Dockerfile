# a small operating system
FROM python:3.9.6-slim
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git-lfs \
    unzip

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV HOST 0.0.0.0
ENV PORT 3000
WORKDIR $APP_HOME

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
COPY model/ /app/model/
RUN unzip /app/model/travelahAlbertCNN.zip -d /app/model

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
