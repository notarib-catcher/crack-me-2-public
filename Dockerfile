FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY . .

EXPOSE 80/tcp

CMD ["gunicorn","-b","0.0.0.0:80","wsgi:app"]

