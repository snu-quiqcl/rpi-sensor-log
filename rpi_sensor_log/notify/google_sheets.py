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
            self.worksheet.insert_row(
                values=[
                    current_time,
                    result.temperature,
                    result.humidity,
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
