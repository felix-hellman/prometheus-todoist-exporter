FROM python:3

ADD exporter.py /
RUN pip3 install todoist-python prometheus_client

CMD [ "python3", "exporter.py" ]
