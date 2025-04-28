"""
surf_forecast.py
This module defines the SurfForecast class, which represents a surf forecast.
"""
import datetime
import numpy as np

class SurfForecast:
    """
    Class to represent a surf forecast.
    """
    OFFSHORE = 105

    def __init__(self, date: datetime, height, period, direction, wind_speed, wind_direction):
        """
        Initialize the surf forecast with date, height, period, direction, wind speed, and wind direction.
        """
        self.date = date
        self.height = height
        self.period = period
        self.direction = direction
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

    def wind_dir(self) -> float:
        """
        returns number representing wind direction in relation to shore
        it is possible to add finer tuning, or switch with polynomial regression altogether
        :param deg: wind direction in degrees
        :return: 1 - offshore, 2 - onshore, 3 - side-offshore, 4 - side-onshore
        """
        EDGE = 121.628
        def midrange(deg:float) -> float:
            """
            the function to apply for winds in the middle of the range
            """
            return -1.5 * np.cos((np.pi / 90) * deg) + 2.5
        def edgecase(deg:float) -> float:
            """
            the function to apply for winds in the edge of the range
            """
            return np.cos((np.pi / 90) * deg) / 1.5 + 0.3
        deg = self.wind_direction-self.OFFSHORE
        if deg > 180:
            deg = deg - 360
        if -EDGE < deg < EDGE:
            return midrange(deg)
        return edgecase(deg)

    def wind_quality(self) -> float:
        """
        Returns the quality of the wind.
        """
        return self.wind_dir() * self.wind_speed / 10
    
    def __str__(self):
        """
        Returns a string representation of the surf forecast.
        """
        return f"Date: {self.date},Height: {self.height}, Period: {self.period},"\
                f" Direction: {self.direction}, Wind Speed: {self.wind_speed},"\
                f" Wind Direction: {self.wind_direction}"
