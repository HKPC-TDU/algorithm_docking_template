FROM python:3.8.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 51001

CMD [ "python3", "manage.py"]