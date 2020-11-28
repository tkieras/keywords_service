
FROM python:3.8-slim-buster as BASE

RUN apt-get update && \
	apt-get install gcc postgresql libpq-dev  -y && \
	apt-get clean

WORKDIR /app

COPY ./requirements.txt ./
RUN pip wheel --wheel-dir=/root/wheels -r ./requirements.txt
RUN pip wheel --wheel-dir=/root/wheels uwsgi


FROM python:3.8-slim-buster as RELEASE

RUN apt-get update && apt-get install unzip

EXPOSE 8080
WORKDIR /app 

COPY --from=BASE /root/wheels /root/wheels
COPY ./dist/ ./dist/
COPY ./nltk_data/archive ./nltk_data/archive
COPY ./uwsgi.ini ./

RUN unzip ./nltk_data/archive/stopwords.zip -d ./nltk_data/corpora && \
    unzip ./nltk_data/archive/wordnet.zip -d ./nltk_data/corpora

ENV NLTK_DATA=/app/nltk_data

RUN apt-get update && \
	apt-get install libpq-dev -y

RUN pip install --no-index --find-links=/root/wheels /root/wheels/* && \
    pip install dist/*

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
