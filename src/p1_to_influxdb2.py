#!/usr/bin/python3

from dsmr_parser import telegram_specifications, obis_references
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import decimal
import time
import click


@click.group()
def main():
    pass


@main.command()
@click.option('--host', '-h')
@click.option('--token', '-t')
@click.option('--organization', '-o')
@click.option('--bucket', '-b')
@click.option('--device', '-d')
def main(host, token, organization, bucket, device):
    connect_to_influx(host, token, organization)

    while True:
        try:
            serial_reader = SerialReader(
                device=device,
                serial_settings=SERIAL_SETTINGS_V4,
                telegram_specification=telegram_specifications.V4
            )

            print("Waiting for P1 port measurement..")

            for telegram in serial_reader.read():
                for key, value in telegram.items():
                    if hasattr(value, "value") and (isinstance(value.value, int) or isinstance(value.value, decimal.Decimal)):
                        name = determine_obis_name(key)
                        measure(bucket, determine_type(key), name, value.value)

        except Exception as e:
            print(str(e))
            print("Pausing and restarting...")
            time.sleep(10)


def connect_to_influx(host, token, organization):
    global write_api
    print("Connecting to database")
    client = InfluxDBClient(url=host,
                            token=token,
                            org=organization)
    write_api = client.write_api(write_options=SYNCHRONOUS)


def determine_obis_name(obis_key):
    result = None
    for obis_name in dir(obis_references):
        if getattr(obis_references, obis_name) == obis_key:
            result = obis_name
            break
    return result


def measure(bucket, measurement_type, measurement_key, measurement_value):
    print(f"Measuring {measurement_key}: {measurement_value}")
    write_api.write(bucket=bucket,
                    record=Point("p1").tag("type", measurement_type).field(measurement_key, float(measurement_value)))


def determine_type(key):
    result = None
    if key == 'HOURLY_GAS_METER_READING':
        result = "gas"
    else:
        result = "power"
    return result


if __name__ == "__main__":
    main()
