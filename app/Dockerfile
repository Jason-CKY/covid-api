FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as base
COPY ./requirements.txt /requirements.txt
COPY ./.env .env
RUN pip install -r /requirements.txt
COPY ./ /app
RUN chmod +x /app/wait-for-it.sh
ENV PYTHONPATH /app

FROM base as test
COPY ./requirements-test.txt /requirements-test.txt
RUN pip install -r /requirements-test.txt

FROM base as loadtest
COPY ./requirements-loadtest.txt /requirements-loadtest.txt
RUN pip install -r /requirements-loadtest.txt