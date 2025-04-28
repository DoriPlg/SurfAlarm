"""
the main module for the surf forecast application, to run every morning, lighting up the right bulbs
"""
from time import sleep
import sys
import RPi.GPIO as GPIO
import forecast_pull
import surf_rate

GPIO.setmode(GPIO.BCM)
# Assign GPIO pins
LEDS = {"GREEN": 17, "YELLOW": 27, "BLUE": 22}

def init_leds():
    """
    Initializes the LEDs
    """
    for led in LEDS.values():
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)

def test():
    """
    Test function to blink the LEDs
    """
    # Blink them for testing
    while True:
        for led in LEDS.values():
            GPIO.output(led, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(led, GPIO.LOW)
            sleep(0.5)

def turn_leds(rate):
    """
    Turns on the appropriate LED based on the surf rate
    :param rate: the surf rate, 0 = no surf, 1 = ok surf, 2 = good surf, -1 = error
    """
    if rate == 0:
        for led in LEDS.values():
            GPIO.output(led, GPIO.LOW)
    elif rate == 1:
        turn_leds(0)
        GPIO.output(LEDS["GREEN"], GPIO.HIGH)
    elif rate == 2:
        turn_leds(0)
        GPIO.output(LEDS["YELLOW"], GPIO.HIGH)
    elif rate == -1:
        turn_leds(0)
        GPIO.output(LEDS["BLUE"], GPIO.HIGH)


def morning_check():
    """
    checks the surf conditions and lights up the appropriate LED
    :return: the surf rate, 0 = no surf, 1 = ok surf, 2 = good surf, -1 = error
    """
    try:
        forecast = forecast_pull.get_upcoming_forecasts()
    except (ValueError, TimeoutError, ConnectionError) as e:
        print(f"Error getting forecast: {e}")
        return -1
    max_rate = 0
    for f in forecast:
        max_rate = max(max_rate, surf_rate.rate_surf_conditions(f))
    return max_rate


if __name__ == "__main__":
    init_leds()
    if len(sys.argv) != 2:
        print("Usage: python main.py [run/halt]")
        sys.exit(1)
    if sys.argv[1].lower() != "run":
        turn_leds(morning_check())
    elif sys.argv[1].lower() != "halt":
        turn_leds(0)
    else:
        print("Usage: python main.py [run/halt]")
        sys.exit(1)
