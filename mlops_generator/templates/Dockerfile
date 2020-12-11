FROM python:3.6-slim-jessie
WORKDIR /{{ project_name }}
COPY ./requirements.txt /{{ project_name }}/requirements.txt
RUN pip install -r /{{ project_name }}/requirements.txt
COPY . /{{ project_name }}
RUN python setup.py install
