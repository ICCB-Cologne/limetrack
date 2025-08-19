FROM python:3.12

RUN apt -y update && apt -y upgrade


COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt