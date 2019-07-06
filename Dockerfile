FROM python:3.7.3-slim

COPY *.py /
COPY requirements.txt /
COPY templates /templates
COPY config.properties.example /config.properties

RUN pip3 install -r /requirements.txt \
	&& rm -rf ~/.cache/pip

EXPOSE 80

ENTRYPOINT ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--reload"]