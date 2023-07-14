FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends 

## add and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["sh", "-c" ,  "python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
