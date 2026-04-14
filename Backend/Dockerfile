From python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requeriments.txt

RUN pip install --no-cached-dir -r requeriments.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
