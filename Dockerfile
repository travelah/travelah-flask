# a small operating system
FROM python:3.9-slim
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
