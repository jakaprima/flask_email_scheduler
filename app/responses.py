import copy
import datetime
from typing import Dict
from flask import request

from .utils import get_timezone, generate_api_call_id
from .messages import (RESPONSE_ERROR, RESPONSE_SUCCESS)


class Response:
    mapping_data = dict(
        id='message_id',
        status='message_action',
        desc='message_desc',
        data='message_data',
        message_request_datetime='message_request_datetime',
    )

    def __init__(self, status, desc, data, timezone='Asia/Singapore'):
        if request and hasattr(request, 'request_unique_id'):
            call_id = request.request_unique_id
        else:
            call_id = generate_api_call_id()

        tz = get_timezone(timezone)
        date_time_obj = datetime.datetime.now(tz)

        self.response = dict(
            id=call_id,
            status=status,
            desc=desc,
            data=data,
            message_id=call_id,
            message_action=status,
            message_desc=desc,
            message_data=data,
            message_request_datetime=date_time_obj.strftime(
                '%Y-%m-%d %H:%M:%S'),
        )

    def put(self, key, value):
        if not (key in self.response):  # pragma: no cover
            raise ValueError('SETTING_NON_EXISTING_FIELD', key, value)

        self.response[key] = value
        self.response[self.mapping_data[key]] = value

    def stringify_v1(self):
        record_prev = copy.deepcopy(self.response)
        del record_prev['status']
        del record_prev['id']
        del record_prev['desc']
        del record_prev['data']
        return record_prev


def process_response_error(message_code: str):  # pragma: no cover
    error_resp = dict()

    errors = RESPONSE_ERROR.get(message_code)

    if errors:
        error_resp['status'] = errors.get('status')
        error_resp['code'] = errors.get('code')
        error_resp['message'] = errors.get('message')

    return error_resp


def construct_error_message(response: Response, code: str):  # pragma: no cover
    error_resp = process_response_error(code)
    response.put('status', error_resp.get('code'))
    response.put('desc', error_resp.get('message'))

    return response, error_resp.get('status')


def wrap_error_message_schema(err_messages: Dict):
    array_resp = list()
    for key, value in err_messages.items():
        err_dict = dict(
            key=key,
            description=value[0] if isinstance(value, list) else value
        )
        array_resp.append(err_dict)

    return array_resp


def process_response(response: Response, action: str, message_code: str):
    resp_config = dict()
    status_code = 200

    if action == 'success':
        resp_config = RESPONSE_SUCCESS.get(message_code)
    if action == 'error':
        resp_config = RESPONSE_ERROR.get(message_code)

    if resp_config:
        response.put('status', resp_config.get('code'))
        response.put('desc', resp_config.get('message'))
        status_code = resp_config.get('status')

    return response, status_code


def init_success_response(message_code: str, timezone: str = 'Asia/Singapore'):
    init_resp = Response("", "", {}, timezone)

    response, status_code = process_response(init_resp, action='success',
                                             message_code=message_code)

    return response, status_code


def init_response(message_code: str, timezone: str = 'Asia/Singapore'):
    init_resp = Response("", "", {}, timezone)

    response, status_code = process_response(init_resp, action='error',
                                             message_code=message_code)

    return response, status_code
