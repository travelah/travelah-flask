# a small operating system
FROM python:3.9.6-slim
RUN pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y curl && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y git-lfs

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt ./

RUN apt-get install -y build-essential && \
    pip install -r requirements.txt

COPY . ./
COPY model/ model/

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

