#!/bin/sh
set -eu

# Move to your project path
cd /path/to/your/project

# Set environment variables (if needed)

# Measure and notify
python -m rpi_sensor_log.monitor \
    --google-sheets-url "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEETS_ID/edit" \
    --google-sheets-worksheet-name "YOUR_WORKSHEET_NAME" \
    adafruit_dht22 \
    --pin-number YOUR_GPIO_PIN_NUMBER \
