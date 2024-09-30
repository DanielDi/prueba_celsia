# Usamos una imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente en el contenedor
COPY . .

# Comando para ejecutar el script
CMD ["python", "main.py"]