FROM python:3.11.4-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip wheel && \
  pip install -r requirements.txt
  
COPY . .

CMD exec gunicorn -k uvicorn.workers.UvicornWorker api:app
