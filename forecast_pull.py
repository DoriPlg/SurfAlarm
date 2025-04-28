"""
This module pulls data from the Stormglass API and returns a dictionary of
the desired sea conditions. It also provides functions to get the tide situation
and a list of conditions for a given time.
"""
from datetime import datetime, timezone, timedelta
import requests # type: ignore
from surf_forecast import SurfForecast


def read_key() -> str:
    """
    Reads the API key from the keys file
    :return: API key as a string
    """
    with open('keysNdata/access_key.txt', 'r', encoding='utf-8') as f:
        return f.read().strip()

DATA_PARAMS =\
    ['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod']
    # tide pulled separately
ACCESS_KEY = read_key()
PULL_PARAMS = {
        'lat': 32.1761,
        'lng': 34.7984,
        'params': ','.join(DATA_PARAMS),
        'start': None,
        'end':  None
    }
PULL_FILEPATH ="keysNdata/pulls.txt"
FORECAST_API_PATH = 'https://api.stormglass.io/v2/weather/point'


def pull_data(timed:datetime = datetime.now(timezone.utc)) -> dict:
    """
    pulls the data from the stormglass API and saves it to a file
    :param forecast_type: str, either "surf" or "tide"
    :param timed: datetime object, the time to pull data for
    :return: dictionary of the data
    :raise: ValueError if forecast_type is not "surf" or "tide"
    :raise: TimeoutError if the request times out
    :raise: ConnectionError if there is a connection error
    """
    # Set the start and end times for the API request, from the given date, five days in the future
    PULL_PARAMS['start'], PULL_PARAMS['end'] = timed, timed+timedelta(days=5)
    api_path = FORECAST_API_PATH
    try:
        response = requests.get(api_path, params=PULL_PARAMS,
                                headers={'Authorization': ACCESS_KEY}, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout as e:
        raise TimeoutError("The request timed out. Please try again later.") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"An error occurred while making the request: {e}") from e
    res = response.json()
    with open(PULL_FILEPATH, 'a', encoding='utf-8') as f:
        f.write(str(res))
    return res


# makes a dictionary of the desired sea conditions
def get_upcoming_forecasts(timed: datetime = datetime.now(timezone.utc)) -> list[SurfForecast]:
    """
    Pulls the data from the stormglass API and returns a dictionary of the desired sea conditions
    If relevant updates the collumn to be a median of the data
    :param timed: datetime object, the time to pull data for
    :return: list of SurfForecast objects
    :raise: ValueError if forecast_type is not "surf" or "tide"
    :raise: TimeoutError if the request times out
    :raise: ConnectionError if there is a connection error
    """
    # Reference data for testing, uncomment to use
    # x = {'hours':
    # [{
    #     'swellDirection': {'dwd': 271.02, 'icon': 268.68, 'noaa': 283.05, 'sg': 268.68},
    #     'swellHeight': {'dwd': 1.98, 'icon': 1.83, 'noaa': 0.35, 'sg': 1.83},
    #     'swellPeriod': {'dwd': 7.11, 'icon': 7.51, 'noaa': 7.64, 'sg': 7.51},
    #     'time': '2023-01-31T10:00:00+00:00',
    #     'windDirection': {'icon': 274.46, 'noaa': 279.5, 'sg': 274.46},
    #     'windSpeed': {'icon': 8.51, 'noaa': 8.3, 'sg': 8.51}
    # }],
    # 'meta':
    # {
    #     'cost': 1, 'dailyQuota': 10, 'end': '2023-01-31 10:20', 'lat': 32.1761, 'lng': 34.7984,
    #     'params': ['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod'],
    #     'requestCount': 10, 'start': '2023-01-31 10:00'
    # }}
    # df = pd.DataFrame(x["hours"][0])
    forecasts = []
    data = pull_data(timed)
    for entry in data["hours"]:
        wind_avg = 0
        for key in entry["windSpeed"]:
            wind_avg += entry["windSpeed"][key]
        wind_avg /= len(entry["windSpeed"])
        forecasts.append(
            SurfForecast(
                date=datetime.fromisoformat(entry["time"]),
                height=entry["swellHeight"]["sg"],
                period=entry["swellPeriod"]["sg"],
                direction=entry["swellDirection"]["sg"],
                wind_speed=wind_avg,
                wind_direction=entry["windDirection"]["sg"]
            ))
    return forecasts
