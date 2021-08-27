FROM python:3

COPY app.py /app/

COPY requirements.txt /app/

COPY start.sh /

COPY config-example.yml /app/config/config.yml

RUN pip install -U pip && \
	pip install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8080

ENV LOGLEVEL="info"

RUN useradd user

USER user

ENTRYPOINT ["bash", "/start.sh"]