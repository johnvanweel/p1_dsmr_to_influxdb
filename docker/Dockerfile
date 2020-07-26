FROM python:3

#RUN apt-get update
#RUN apt-get install -y python3 python3-pip
RUN pip install dsmr-parser
RUN pip install influxdb-client
RUN pip install click

COPY *.py /tmp/p1/

WORKDIR /tmp/p1/

CMD ["sh", "-c", "python3 -u /tmp/p1/p1_to_influxdb2.py -h ${host} -o ${organization} -d ${device} -b ${bucket} -t ${token}"]