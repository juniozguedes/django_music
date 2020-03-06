FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /django_music
WORKDIR /django_music
COPY requirements.txt /django_music/
RUN pip install -r requirements.txt
COPY . /django_music/