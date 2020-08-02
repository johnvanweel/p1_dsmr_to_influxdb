FROM python:3

RUN pip install click
RUN pip install paho-mqtt
RUN pip install influxdb-client

COPY *.py /tmp/p1/

WORKDIR /tmp/p1/

CMD ["sh", "-c", "python3 -u /tmp/p1/mqtt_to_influx.py -h ${host} -o ${organization} -b ${bucket} -t ${token}"]