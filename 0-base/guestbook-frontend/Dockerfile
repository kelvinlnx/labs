FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update

RUN apt-get upgrade -y

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
