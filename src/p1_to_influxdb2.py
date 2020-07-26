#!/usr/bin/python3

from dsmr_parser import telegram_specifications, obis_references
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pprint
import config
import decimal
import time

prev_gas = None
bucket = "home_automation"

# influx db settings
print("Connecting to database")
client = InfluxDBClient(url=config.host,
                        token="X62MRNnOM5R8EuUN4zVe7i3pxt60OK0yYSVD24yuR3edGz5ZvFrUP8GvDVofydFiwGP4zp-GEeJrCuzI_fH4lw==",
                        org="home")
write_api = client.write_api(write_options=SYNCHRONOUS)


def determine_obis_name():
    result = None
    for obis_name in dir(obis_references):
        if getattr(obis_references, obis_name) == key:
            result = obis_name
            break
    return result


def measure(measurement_type, measurement_key, measurement_value):
    print(f"Measuring {measurement_key}: {measurement_value}")
    write_api.write(bucket=bucket,
                    record=Point("p1").tag("type", measurement_type).field(measurement_key, float(measurement_value)))


while True:
    try:
        serial_reader = SerialReader(
            device=config.serial_port,
            serial_settings=SERIAL_SETTINGS_V4,
            telegram_specification=telegram_specifications.V4
        )

        print("Waiting for P1 port measurement..")

        for telegram in serial_reader.read():
            for key, value in telegram.items():
                if hasattr(value, "value"):
                    name = determine_obis_name()

                    if isinstance(value.value, int) or isinstance(value.value, decimal.Decimal):
                        if key == 'HOURLY_GAS_METER_READING':
                            measure("gas", name, value.value)
                        else:
                            measure("power", name, value.value)
    except Exception as e:
        print(str(e))
        print("Pausing and restarting...")
        time.sleep(10)
