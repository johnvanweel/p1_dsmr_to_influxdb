import paho.mqtt.client as mqtt
import click
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

influx_bucket = None
write_api = None


@click.group()
def main():
    pass


@main.command()
@click.option('--host', '-h')
@click.option('--token', '-t')
@click.option('--organization', '-o')
@click.option('--bucket', '-b')
def main(host, token, organization, bucket):
    global influx_bucket
    influx_bucket = bucket
    connect_to_influx(host, int(32999), token, organization)

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(host, int(32184))
    print("Connected to MQTT")
    mqtt_client.loop_forever()


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server.")
    client.subscribe("/sensor/p1/#")


def on_message(client, userdata, message):
    global influx_bucket
    key = message.topic[message.topic.rindex("/")+1:]
    value = float(message.payload)
    try:
        measure(influx_bucket, determine_type(key), key, value)
    except Exception as e:
        print(e)
        pass


def measure(bucket, measurement_type, measurement_key, measurement_value):
    write_api.write(bucket=bucket,
                    record=Point("p1").tag("type", measurement_type).field(measurement_key, float(measurement_value)))


def determine_type(key):
    result = None
    if key == 'HOURLY_GAS_METER_READING':
        result = "gas"
    else:
        result = "power"
    return result


def connect_to_influx(host, port, token, organization):
    global write_api
    print("Connecting to database")
    client = InfluxDBClient(url=f"http://{host}:{port}",
                            token=token,
                            org=organization)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("Connected to database")


if __name__ == "__main__":
    main()
