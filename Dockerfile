FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir discord.py mysql-connector

COPY . .

CMD [ "python", "./main.py" ]