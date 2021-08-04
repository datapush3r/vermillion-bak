FROM python:3.6

WORKDIR /opt/vermillion

COPY manage.py gunicorn-cfg.py requirements.txt .env ./
COPY app app
COPY core core

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 80
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]