# Imagen base ligera
FROM python:3.11-slim

# Evita buffer en stdout/stderr
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Variables de entorno (sobrescribe en EasyPanel)
ENV MS_TOKEN=""
ENV DEVICE_ID=""

# Puerto interno
EXPOSE 8000

# Comando de arranque
CMD ["python", "main.py"]
