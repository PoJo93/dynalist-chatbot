# coding: utf-8

import os
import recastai
from flask import request
import requests

from flask import jsonify

#Custom libraries
import json


def post_to_inbox(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    print(request_content)
    message = request_content['nlp']['source']

    dynalist_token = request_content['conversation']['memory']['token']
    #dynalist_token = 'WhqJkcbexDdQEl87cA5lEy2hFNIokQkj9iOev-ag7EJAPyUSDipPrzb0Hz6yJ9J6oIbyghDi_t_rWBUlS99CdnFCAixGnjko_4KUfZQpaIG4z0pcHVnWAgu53G1887SF'
    dynalist_payload = {
                          "token": dynalist_token,
                          "index": 0,
                          "content": message,
                          "note": "",
                          "checked": False
                        }
    r = requests.post('https://dynalist.io/api/v1/inbox/add', json=dynalist_payload)
    return jsonify(status=200)


def check_token_request(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    print(request_content)

    dynalist_token = request_content['conversation']['memory']['token']
    #dynalist_token = 'WhqJkcbexDdQEl87cA5lEy2hFNIokQkj9iOev-ag7EJAPyUSDipPrzb0Hz6yJ9J6oIbyghDi_t_rWBUlS99CdnFCAixGnjko_4KUfZQpaIG4z0pcHVnWAgu53G1887SF'
    dynalist_payload = {
                          "token": dynalist_token
                        }
    r = requests.post('https://dynalist.io/api/v1/inbox/add', json=dynalist_payload)
    return jsonify(status=200)
