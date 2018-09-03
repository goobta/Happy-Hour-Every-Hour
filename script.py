import datetime
from math import sin, cos, radians
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }


def get_location_for_time(time):
    wpi_lat = 42.2746
    wpi_long = 71.8063

    current_date = datetime.datetime.now()

    if is_hour_forward(current_date):
        delta = -4
    else:
        delta = -5

    days_delta = datetime.date(current_date.year, 1, 1) - current_date.date()
    days_delta = abs(days_delta.days)

    B = radians((days_delta - 81) * 360 / 365)
    E = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.58 * sin(B)
    time_correction = 4 * (delta * 15 + wpi_lat) + E

    adjusted_time = current_date + datetime.timedelta(minutes=time_correction)
    difference = time - adjusted_time

    print(adjusted_time)
    print(difference)

    lon_change = (difference.days * 24 * 60 * 60 + difference.seconds) * \
            15 / 60 ** 2
    
    print(lon_change)
    adjusted_lon = -wpi_long + lon_change
    return adjusted_lon

def is_hour_forward(t):
    if t.month < 3 or t.month > 11:
        return False
    elif t.month > 3 and t.month < 11:
        return True
    elif t.month == 3:
        second_sunday = (7 - datetime.datetime(t.year, 3, 1).weekday()) % 7 + 7
        return t.day >= second_sunday
    elif t.month == 11:
        first_sunday = (7 - datetime.datetime(t.year, 11, 1).weekday()) % 7
        return t.day <= first_sunday

current_date = datetime.datetime.now()
print(get_location_for_time(datetime.datetime(
    current_date.year,
    current_date.month,
    current_date.day,
    17,
    0,
    0)))
