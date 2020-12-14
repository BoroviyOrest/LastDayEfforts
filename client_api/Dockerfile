FROM python:3.7

RUN mkdir client_api

WORKDIR client_api

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
