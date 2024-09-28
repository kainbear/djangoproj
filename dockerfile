# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]