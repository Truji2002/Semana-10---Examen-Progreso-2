FROM python:3.10-slim

WORKDIR /app

# Copiar los archivos necesarios
COPY app/soap_service.py ./soap_service.py
COPY app/database.py ./database.py
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "soap_service.py"]
