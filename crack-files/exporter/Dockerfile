FROM python:latest

WORKDIR /app
COPY . /app
RUN pip install awscli boto3

ENTRYPOINT ["python", "export.py"]
