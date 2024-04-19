FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-traditional

COPY src/api/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/entrypoint.sh .
COPY src/api api/

ENTRYPOINT ["/app/entrypoint.sh"]