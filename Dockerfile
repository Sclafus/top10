FROM python:3.11

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "app.__main__:app", "--bind", "0.0.0.0:5000"]
