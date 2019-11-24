import datetime


def get_timestamp_from_iso(iso_date):
    dt = datetime.datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(dt.timestamp())
