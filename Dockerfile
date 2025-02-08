FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app/main.py"]
