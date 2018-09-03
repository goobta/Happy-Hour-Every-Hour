import datetime
import requests
import json

def lambda_handler(event, context):
    ret_str = ""

    if event['request']['intent']['name'] == 'SearchIntent':
        time_str = event['request']['intent']['slots']['time']['value']

        current_time = datetime.datetime.utcnow()
        if ":" in time_str:
            t = datetime.datetime.strptime(time_str, "%H:%M")
        else:
            t = datetime.datetime.strptime(time_str, "%H")

        time = t.replace(
            year=current_time.year,
            month=current_time.month,
            day=current_time.day)

        ret_str = get_location_for_time(time)
    elif event['request']['intent']['name'] == "HappyHourIntent":
        current_time = datetime.datetime.utcnow()
        hh_time = current_time.replace(hour=17, minute=0)

        ret_str = get_location_for_time(hh_time)

    elif event['request']['intent']['name'] == "BlazeItIntent":
        current_time = datetime.datetime.utcnow()
        bi_time = current_time.replace(hour=16, minute=20)

        ret_str = get_location_for_time(bi_time)

    return {
        "version": "1.0",
        "statusCode": 200,
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": ret_str,
                "playBehavior": "REPLACE_ENQUEUED"  
            }
        }
    }


def get_location_for_time(time):
    pm_lat = 51.4777
    pm_lon = 0.0004

    current_date = datetime.datetime.utcnow()
    difference = (time.hour - current_date.hour) * 60 + \
            (time.minute - current_date.minute)

    lon_change = difference * (15 / 60)
    adjusted_lon = pm_lon + lon_change

    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor=false".format(
        lat=pm_lat,
        lon=adjusted_lon
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)

    reply = format_res(response.json(), pm_lat, adjusted_lon, time)
    return reply

def format_res(res, lat, lon, time):
    if len(res['results']) == 0:
        if lat > 0: 
            lat_suffix = "north"
        else:
            lat_suffix = "south"

        if lon > 0:
            lon_suffix = "east"
        else:
            lon_suffix = "west"

        location_str = "{:.2f} degrees {} and {:.2f} degrees {}".format(
                abs(lat),
                lat_suffix,
                abs(lon),
                lon_suffix
            )

        return "It is currently {} at {}, which is inhabited by humans".format(
                format_time(time),
                location_str
            )
    else:
        result = res['results'][0]
        location = result['formatted_address']

        return "It is currently {} at {}".format(
                format_time(time),
                location
            )

def format_time(time):
    if time.minute == 0:
        return str(time.hour) + " hundred hours"
    else:
        return "{} {}".format(time.hour, time.minute)

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
    20,
    0,
    0)))
