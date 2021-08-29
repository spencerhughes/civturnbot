FROM python:3

COPY requirements.txt /app/

RUN pip install -U pip && \
	pip install -r /app/requirements.txt

COPY config-example.yml /app/config/config.yml

COPY app.py /app/

WORKDIR /app

EXPOSE 8080

ENV LOGLEVEL="info"

RUN useradd user

USER user

CMD ["gunicorn", "app:app", "--bind 0.0.0.0:8080", "--log-level=$LOGLEVEL", "--workers=4"]