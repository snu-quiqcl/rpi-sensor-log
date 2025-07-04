"""Module for base sensor class."""

from dataclasses import dataclass

@dataclass
class SensorResult:
    """Sensor result class.
    
    Fields:
        success: Whether the measurement was successful.
        error: Error message if the measurement failed.
    """
    success: bool
    error: str | None = None


class Sensor:
    """Base sensor class.
    
    Attributes:
        name: Sensor name.
    """
    
    def __init__(self, name: str):
        """
        Args:
            See Attributes section.
        """
        self.name = name

    def measure(self) -> SensorResult:
        """Measures from sensor and returns the result."""
        raise NotImplementedError('This method must be implemented.')
