FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD echo "Running migrations..." && sleep 10 && python manage.py migrate && echo "Migrations completed" && python manage.py runserver 0.0.0.0:8000
