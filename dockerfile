FROM python:3.12.2

RUN apt-get update && apt-get install -y build-essential libyaml-dev

WORKDIR /djangoproj/testcase

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ptvsd
RUN pip install --upgrade pip setuptools wheel

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]