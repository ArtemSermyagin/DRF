FROM python:3

WORKDIR /DRF

COPY ./requirements.txt /DRF/

RUN pip install -r requirements.txt

COPY . .

