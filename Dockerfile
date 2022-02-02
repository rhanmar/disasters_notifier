FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000