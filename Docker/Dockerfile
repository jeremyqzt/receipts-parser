FROM python:3.8.13-slim

RUN mkdir /srv/flask_app

COPY . /srv/flask_app
WORKDIR /srv/flask_app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install tesseract-ocr -y
RUN apt-get install --no-install-recommends build-essential curl libpq-dev -y
RUN apt-get clean 
RUN pip3 install -r requirements.txt

COPY nginx.conf /etc/nginx
RUN chmod +x ./startup.sh

EXPOSE 80
CMD ["./startup.sh"]