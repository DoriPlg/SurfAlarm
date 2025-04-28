"""
surf_rate.py
This module defines the rating system for surf conditions.
"""

from surf_forecast import SurfForecast

GOOD_PERIOD = 8.5
BAD_PERIOD = 6.5
GOOD_HEIGHT = 1.4
BAD_HEIGHT = 0.8
GOOD_WIND = 2.4
BAD_WIND = 6.5

def rate_surf_conditions(surf_forecast: SurfForecast) -> str:
    """
    Rate the surf conditions based on the surf forecast.
    :param surf_forecast: SurfForecast object
    :return: "good" if at least two parameters are in their good range, otherwise "bad"
    """
    # Create a boolean vector for each condition
    good_conditions = [
        surf_forecast.period >= GOOD_PERIOD,
        surf_forecast.height >= GOOD_HEIGHT,
        surf_forecast.wind_quality() <= GOOD_WIND
    ]
    # Count how many conditions are good
    if sum(good_conditions) >= 2:
        return 2
    # Create a boolean vector for bad conditions
    bad_conditions = [
        surf_forecast.period <= BAD_PERIOD,
        surf_forecast.height <= BAD_HEIGHT,
        surf_forecast.wind_quality() >= BAD_WIND
    ]
    # Count how many conditions are bad
    if sum(bad_conditions) >= 2:
        return 0
    # If neither condition is met, return 1
    return 1
