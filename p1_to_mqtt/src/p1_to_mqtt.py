#!/usr/bin/python3

import decimal
import time

import click
import paho.mqtt.client as paho
from dsmr_parser import telegram_specifications, obis_references
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4


@click.group()
def main():
    pass


@main.command()
@click.option('--host', '-h')
@click.option('--mqtt-port', '-pm')
@click.option('--topic', '-t')
@click.option('--device', '-d')
def main(host, port, topic, device):
    mqtt = paho.Client("pirate")

    while True:
        try:
            serial_reader = SerialReader(
                device=device,
                serial_settings=SERIAL_SETTINGS_V4,
                telegram_specification=telegram_specifications.V4
            )

            print("Waiting for P1 port measurement..")

            for telegram in serial_reader.read():
                measurement = {}
                for key, value in telegram.items():
                    if hasattr(value, "value") and (
                            isinstance(value.value, int) or isinstance(value.value, decimal.Decimal)):
                        name = determine_obis_name(key)
                        measurement[name] = float(value.value)

                for key, value in measurement.items():
                    # Need to connect each time, or for some reason it disconnects without Exception
                    mqtt.connect(host=host, port=port)
                    mqtt.publish(topic=topic + "/" + key, payload=value)
                    mqtt.disconnect()

        except Exception as e:
            print(str(e))
            print("Pausing and restarting...")
            time.sleep(10)


def determine_obis_name(obis_key):
    result = None
    for obis_name in dir(obis_references):
        if getattr(obis_references, obis_name) == obis_key:
            result = obis_name
            break
    return result


if __name__ == "__main__":
    main()
