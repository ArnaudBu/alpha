FROM python:3.8-slim-buster

COPY run.py gunicorn.py requirements.txt config.py .env ./

RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations

EXPOSE 5000
CMD ["gunicorn", "--config", "gunicorn.py", "run:app"]