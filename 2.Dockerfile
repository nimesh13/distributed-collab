FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py" , "--port=8001", "--connect_port=8000", "--connect_host=a.b.c.d"]