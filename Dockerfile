FROM python:3.7.1

RUN mkdir /hnit-acm-web

COPY . /hnit-acm-web

WORKDIR /

RUN mkdir ~/.pip

RUN cp ./hnit-acm-web/pip.conf ~/.pip/

RUN pip install -r ./hnit-acm-web/requirements.txt

CMD ["python", "./hnit-acm-web/app.py"]
