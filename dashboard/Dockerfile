FROM python:3.12.3-slim-bookworm
RUN apt-get update
RUN apt-get install nano

RUN mkdir wd
WORKDIR wd
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY ./ ./
 
CMD ["gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]