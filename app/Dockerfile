FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as base
COPY ./requirements.txt /requirements.txt
COPY ./.env .env
RUN pip install -r /requirements.txt
COPY ./ /app
ENV PYTHONPATH /app