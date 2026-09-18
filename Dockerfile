FROM python:3.14

RUN apt-get update &&  \
    apt-get install -y wait-for-it

RUN mkdir /ecommerce

WORKDIR /ecommerce

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /ecommerce/docker/*.sh
