# استخدام Python 3.11 كصورة أساسية
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# تثبيت المتطلبات الأساسية للنظام
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات
COPY requirements_clean.txt requirements.txt

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تثبيت mention إذا لم يكن موجوداً
RUN pip install mention || echo "mention package not found, continuing..."

# نسخ ملفات التطبيق
COPY . .

# إنشاء مجلد الصور
RUN mkdir -p iage

# تعيين متغير البيئة للبايثون
ENV PYTHONUNBUFFERED=1

# تشغيل اليوزر بوت
CMD ["python", "main.py"]

