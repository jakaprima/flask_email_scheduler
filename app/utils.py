import datetime
import random
import time
import uuid

import pytz


def generate_api_call_id():
    """
    Generate unique api call id
    """
    now_time = int(time.time())
    current_date = datetime.datetime.now()

    hour_tm = current_date.hour
    minute_tm = current_date.minute
    second_tm = current_date.second

    start_id = str(now_time) + str(hour_tm) + str(minute_tm) + str(second_tm)
    random_num = random.randint(1, 10000000)
    invoice_code = 'API_CALL_{}_{}'.format(str(start_id), str(random_num))
    return invoice_code


def get_timezone(timezone: str) -> pytz.timezone:
    try:
        tz = pytz.timezone(timezone)
        return tz
    except Exception:  # pragma: no cover
        return pytz.timezone('Asia/Singapore')


def generate_random_id() -> str:  # pragma: no cover
    """ generate random id -> length 32"""
    return str(uuid.uuid4().hex)


def generate_random_uuid4() -> str:  # pragma: no cover
    """ generate random uuid4 -> length 36"""
    return str(uuid.uuid4())
