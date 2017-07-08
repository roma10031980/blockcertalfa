FROM python:3.5

ADD . /BlockcertAlfa

WORKDIR /BlockcertAlfa

RUN pip install -r requirements.txt
