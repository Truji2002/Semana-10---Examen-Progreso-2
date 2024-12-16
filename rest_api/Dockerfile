FROM python:3.10-slim

WORKDIR /app

# Copiar los archivos necesarios
COPY app/rest_service.py ./rest_service.py
COPY app/database.py ./database.py
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "rest_service.py"]
