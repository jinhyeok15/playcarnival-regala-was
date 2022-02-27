FROM python:3
WORKDIR /app
ADD . /app
RUN apt-get update
RUN apt-get install -y python-dev
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get install -y default-mysql-client
CMD ["uwsgi", "uwsgi.ini"]
