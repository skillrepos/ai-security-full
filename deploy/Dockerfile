# Sample Dockerfile to be scanned by the Lab 8 security gate.
# It intentionally contains a few bad practices for the lab to catch.
FROM python:latest

COPY . /app
WORKDIR /app

RUN pip install -r app/requirements_app.txt

CMD ["python", "app/app.py"]
