# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /backend

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY main.py .

CMD [ "python", "main.py" ]