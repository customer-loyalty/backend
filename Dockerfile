FROM python:3.10.9-slim

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "system.wsgi:application", "--bind", "0:8000"]

