FROM python:3

#RUN apt-get update
#RUN apt-get install -y python3 python3-pip
RUN pip install dsmr-parser
RUN pip install influxdb-client

COPY *.py /tmp/p1/

WORKDIR /tmp/p1/

CMD ["python3", "-u", "/tmp/p1/p1_to_influxdb2.py"]
#CMD ["ls", "/tmp/"]