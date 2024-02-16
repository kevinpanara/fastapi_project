FROM public.ecr.aws/docker/library/python:3.11

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./alembic.ini /
RUN mkdir /app
COPY ./app/ /app/

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
