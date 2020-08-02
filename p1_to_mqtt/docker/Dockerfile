FROM python:3

RUN pip install dsmr-parser
RUN pip install click
RUN pip install paho-mqtt

COPY *.py /tmp/p1/

WORKDIR /tmp/p1/

CMD ["sh", "-c", "python3 -u /tmp/p1/p1_to_mqtt.py -h ${host} -pm ${mqtt-port} -t ${topic} -d ${device}"]