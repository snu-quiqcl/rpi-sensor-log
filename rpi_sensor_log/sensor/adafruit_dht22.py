"""Module for Adafruit DHT22 sensor."""

import time
from dataclasses import dataclass

import adafruit_dht
import board

from rpi_sensor_log.sensor.sensor import Sensor, SensorResult

@dataclass
class AdafruitDHT22Result(SensorResult):
    """Adafruit DHT22 sensor result class.
    
    Fields:
        temperature: Temperature.
        humidity: Humidity.
    """
    temperature: float | None = None
    humidity: float | None = None


class AdafruitDHT22(Sensor):
    """Adafruit DHT22 sensor class.
    
    Attributes:
        device: DHT22 device.
        pin: GPIO pin.
    """

    def __init__(self, name: str, pin_number: int):
        """Extended.
        
        Args:
            pin_number: GPIO pin number.
        """
        super().__init__(name)
        try:
            self.pin = getattr(board, f'D{pin_number}')
        except AttributeError:
            raise ValueError(f'Invalid pin number: {pin_number}')

    def _measure_single(self) -> AdafruitDHT22Result:
        """Performs a single measurement and returns the result."""
        try:
            device = adafruit_dht.DHT22(self.pin)
            temperature = device.temperature
            humidity = device.humidity
        except Exception as e:
            print(e)
            result = AdafruitDHT22Result(
                success=False,
            )
        else:
            result = AdafruitDHT22Result(
                success=True,
                temperature=temperature,
                humidity=humidity,
            )
        finally:
            device.exit()
        time.sleep(2)
        return result

    def measure(self) -> AdafruitDHT22Result:
        """Overridden."""
        total_temperature = 0
        total_humidity = 0
        num_measurements = 0
        for _ in range(5):
            result = self._measure_single()
            if not result.success:
                continue
            total_temperature += result.temperature
            total_humidity += result.humidity
            num_measurements += 1
        if num_measurements == 0:
            return AdafruitDHT22Result(
                success=False,
                error='Failed to measure temperature and humidity.',
            )
        return AdafruitDHT22Result(
            success=True,
            temperature=total_temperature / num_measurements,
            humidity=total_humidity / num_measurements,
        )
