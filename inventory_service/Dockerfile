FROM python:3.10-slim

WORKDIR /app

# Copiar los archivos necesarios
COPY app/inventory_service.py ./inventory_service.py
COPY app/database.py ./database.py
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "inventory_service.py"]
