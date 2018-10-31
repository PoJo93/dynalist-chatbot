# coding: utf-8

import os
import recastai
from flask import request
import requests

from flask import jsonify

#Custom libraries
import json


def bot(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    print(request_content)
    message = request_content['conversation']['memory']['message_content']

    dynalist_token = 'WhqJkcbexDdQEl87cA5lEy2hFNIokQkj9iOev-ag7EJAPyUSDipPrzb0Hz6yJ9J6oIbyghDi_t_rWBUlS99CdnFCAixGnjko_4KUfZQpaIG4z0pcHVnWAgu53G1887SF'
    dynalist_payload = {
                          "token": dynalist_token,
                          "index": 0,
                          "content": "Get the book recommended by Jerry",
                          "note": "Should be available in the city library, or on Amazon for around $25",
                          "checked": False
                        }

    r = requests.post('https://dynalist.io/api/v1/inbox/add', json=dynalist_payload)
    return jsonify(status=200)
