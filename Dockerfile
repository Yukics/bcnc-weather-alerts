FROM python:3.11.4-slim-bullseye

WORKDIR /app

COPY ./app/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]