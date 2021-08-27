FROM python:3

COPY requirements.txt /app/

RUN pip install -U pip && \
	pip install -r /app/requirements.txt

COPY app.py /app/

COPY start.sh /

COPY config-example.yml /app/config/config.yml

WORKDIR /app

EXPOSE 8080

ENV LOGLEVEL="info"

RUN useradd user

USER user

ENTRYPOINT ["bash", "/start.sh"]