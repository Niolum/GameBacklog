FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /gamebacklog
COPY requirements.txt /gamebacklog/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /gamebacklog/
EXPOSE 8000