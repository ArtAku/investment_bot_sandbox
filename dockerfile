FROM python:3.10
WORKDIR /app
COPY ./*.py .

ENTRYPOINT [ "python", "main.py" ]