FROM python:3

RUN pip install click
RUN pip install paho-mqtt
RUN pip install influxdb-client

COPY *.py /tmp/p1/

WORKDIR /tmp/p1/

CMD ["sh", "-c", "python3 -u /tmp/p1/p1_to_influxdb2.py -h ${host} -pi ${infux_port} -pm ${mqtt_port} -o ${organization} -b ${bucket} -t ${token}"]