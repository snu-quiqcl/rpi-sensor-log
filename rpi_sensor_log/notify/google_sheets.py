"""Module for logging to Google Sheets."""

import datetime

import gspread
from gspread.utils import ValueInputOption

from rpi_sensor_log.notify.notifier import Notifier
from rpi_sensor_log.sensor.sensor import SensorResult

class GoogleSheetsNotifier(Notifier):
    """Notifier for Google Sheets.
    
    Attributes:
        worksheet: Google Sheets worksheet.
    """

    def __init__(self, url: str, worksheet_name: str):
        """Extended.
        
        Args:
            url: URL of the Google Sheets.
            worksheet_name: Name of the worksheet.
        """
        super().__init__()
        try:
            gc = gspread.service_account()
            sh = gc.open_by_url(url)
            self.worksheet = sh.worksheet(worksheet_name)
        except Exception as e:
            raise ValueError(f'Failed to open Google Sheets: {e}')

    def notify(self, result: SensorResult):
        """Notify the result to Google Sheets."""
        current_time = datetime.datetime.now().isoformat()
        if result.success:
            base_fields = set(SensorResult.__dataclass_fields__.keys())
            sensor_fields = set(result.__dataclass_fields__.keys())
            measurand_fields = sorted([field for field in sensor_fields - base_fields])
            self.worksheet.insert_row(
                values=[
                    current_time,
                    *[getattr(result, field) for field in measurand_fields],
                    '',
                ],
                index=2,
                value_input_option=ValueInputOption.user_entered,
            )
        else:
            self.worksheet.insert_row(
                values=[
                    current_time,
                    '',
                    '',
                    result.error,
                ],
                index=2,
                value_input_option=ValueInputOption.user_entered,
            )
