"""Module for base notifier class."""

from rpi_sensor_log.sensor.sensor import SensorResult

class Notifier:
    """Base notifier class."""

    def notify(self, result: SensorResult):
        """Notify the result.
        
        Args:
            result: Measurement result.
        """
        raise NotImplementedError('This method must be implemented.')
