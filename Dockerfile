FROM python:3.10

COPY . /APP

WORKDIR /APP

RUN python3 -m pip install -r requirements.txt

COPY .env /app/.env

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

EXPOSE 8000:8000

CMD ["python3", "manage.py", "runserver"]