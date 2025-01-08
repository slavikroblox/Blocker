from datetime import datetime
import pytz

def ConvertTimestamp(timestamp_str, desired_timezone='Etc/GMT-3', output_format="%d/%m/%Y, %I:%M %p"):
    timestamp_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    timestamp_datetime = datetime.strptime(timestamp_str, timestamp_format)
    timestamp_datetime_utc = timestamp_datetime.replace(tzinfo=pytz.UTC)

    current_time = datetime.now()
    
    desired_timezone_obj = pytz.timezone(desired_timezone)
    timestamp_datetime_desired_tz = timestamp_datetime_utc.astimezone(desired_timezone_obj)

    formatted_timestamp = timestamp_datetime_desired_tz.strftime(output_format)
    return formatted_timestamp