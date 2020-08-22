FROM python:3.7

RUN pip install pymodbustcp mysql-connector-python

ADD main.py /

CMD [ "python", "/main.py" ]