FROM python:3.7

RUN mkdir ml_api

WORKDIR ml_api

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD uvicorn main:app --reload --host=0.0.0.0
