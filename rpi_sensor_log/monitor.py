"""
Module for monitoring through Raspberry Pi.

- Measuring from sensors.
- Logging to Google Sheets.
"""

import argparse

from rpi_sensor_log.sensor.adafruit_dht22 import AdafruitDHT22
from rpi_sensor_log.notify.google_sheets import GoogleSheetsNotifier

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monitor through Raspberry Pi.')
    parser.add_argument(
        '--google-sheets-url',
        type=str,
        required=True,
        help='Google Sheets URL.',
    )
    parser.add_argument(
        '--google-sheets-worksheet-name',
        type=str,
        required=True,
        help='Google Sheets worksheet name.',
    )
    sensor_parser = parser.add_subparsers(
        dest='sensor_type',
        required=True,
        help='Type of measuring sensor.',
    )
    adafruit_dht22_parser = sensor_parser.add_parser(
        'adafruit_dht22',
        help='Adafruit DHT22 sensor.',
    )
    adafruit_dht22_parser.add_argument(
        '--pin-number',
        type=int,
        required=True,
        help='GPIO pin number.',
    )
    args = parser.parse_args()
    if args.sensor_type == 'adafruit_dht22':
        sensor = AdafruitDHT22(args.pin_number)
    else:
        raise ValueError(f'Unknown sensor type: {args.sensor_type}')
    result = sensor.measure()
    notifier = GoogleSheetsNotifier(args.google_sheets_url, args.google_sheets_worksheet_name)
    notifier.notify(result)
