FROM python:3.7-alpine
# Create an application directory
WORKDIR /tmp

RUN pip3 install \
    flask \
    flask_restx \
    flask-restful


WORKDIR /usr/src/app

COPY . .


ENV FLASK_APP=main.py
EXPOSE 5003
ENTRYPOINT ["flask", "run", "--host=0.0.0.0:5003"]