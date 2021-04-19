FROM python:3.8-slim-buster

ADD Pipfile /opt/image_tagging

ADD . /opt/image_tagging

WORKDIR /opt/image_tagging

RUN python -m venv /opt/image_tagging/.venv && pip install pipenv && pipenv install --dev && mkdir -p /opt/image_tagging/data

ENTRYPOINT ["pipenv", "run", "python", "/opt/image_tagging/main.py"]
