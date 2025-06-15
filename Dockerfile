# Gunakan image python resmi
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin requirements dan install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Expose port Flask (Gunicorn akan listen di 0.0.0.0:8080)
EXPOSE 8080

# Jalankan aplikasi menggunakan gunicorn
CMD ["gunicorn", "web_app:app", "--bind", "0.0.0.0:8080"]
