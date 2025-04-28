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

def init_leds()->None:
    """
    Initializes the LEDs
    """
    for color, led in LEDS.items():
        GPIO.setup(led, GPIO.OUT)
        led_cont(color,False)

def led_cont(color:str, on: bool, disconnect:bool=False)->None:
    """
    Control the led of the specified color
    :param color: the color of the led to control
    :param on: true for on, false for off
    :param disconnect: is we are in the disconnected version
    """
    if disconnect:
        print(f"The {color} led is now {"on" if on else "off"}")
    else:
        GPIO.output(LEDS[color.capitalize()], GPIO.HIGH if on else GPIO.LOW)

def test()->None:
    """
    Test function to blink the LEDs
    """
    # Blink them for testing
    while True:
        for color in LEDS:
            led_cont(color,True)
            sleep(0.5)
            led_cont(color,False)
            sleep(0.5)

def turn_leds(rate: int)->None:
    """
    Turns on the appropriate LED based on the surf rate
    :param rate: the surf rate, 0 = no surf, 1 = ok surf, 2 = good surf, -1 = error
    """
    if rate == 0:
        for color in LEDS:
            led_cont(color,False)
    elif rate == 1:
        turn_leds(0)
        led_cont("YELLOW",True)
    elif rate == 2:
        turn_leds(0)
        led_cont("GREEN",True)
    elif rate == -1:
        turn_leds(0)
        led_cont("BLUE",True)


def morning_check()->int:
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
