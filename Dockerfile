FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers=2 --bind 0.0.0.0:8000 kittens.wsgi"]

EXPOSE 8000