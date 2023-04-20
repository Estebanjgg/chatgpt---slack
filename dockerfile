# Utiliza la imagen oficial de Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al directorio de trabajo
COPY . .

# Ejecuta tu aplicación con el comando predeterminado
CMD ["python", "app.py"]