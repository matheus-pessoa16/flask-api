FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add libffi-dev

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN python -m pip install -r requirements.txt

ENV ENV_FILE_LOCATION ./.envrc

EXPOSE 5000

CMD ["python", "app.py" ]