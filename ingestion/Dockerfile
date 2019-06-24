FROM python:stretch

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./execute.sh

CMD ["./execute.sh"]
