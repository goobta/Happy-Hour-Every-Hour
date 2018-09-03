import datetime
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }


def get_location_for_time(time):
    current_date = datetime.datetime.now()
    dst_start = datetime.date(current_date.year, 3, 11)
    dst_end = datetime.date(current_date.year, 11, 4)

    if current_date.month >= 3 and current_date.month >= 11:
        delta = 4
    elif current_date.month:
        pass

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
