# Python 3.12.4 image kullan
FROM python:3.12.4

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyalarını kopyala ve yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y bash coreutils
# Proje dosyalarını kopyala
COPY . /app/

# Django ayarlarını belirle (örneğin: production ayar dosyası)
ENV DJANGO_SETTINGS_MODULE=api.settings

