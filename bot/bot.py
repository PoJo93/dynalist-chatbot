# coding: utf-8

import os
import recastai
from flask import request
import requests

from flask import jsonify
#Custom libraries
import json


def post_to_inbox(payload):
    print("inbox was activated")

    return request_dynalist(payload, 'https://dynalist.io/api/v1/inbox/add', False)

def check_token_request(payload ):
    print("Check TOken was activated")
    return request_dynalist(payload, 'https://dynalist.io/api/v1/file/list', True)


def request_dynalist(payload, api_adress, check_token_only):
    channel, timestamp, message, token, conversation_memory = extract_content(payload)
    note = build_dynalist_note(channel=channel,contact=None,timestamp=timestamp )
    payload = build_dynalist_payload(token, message, check_token_only, note)
    response = call_dynalist_api(api_adress, payload )
    return build_recast_response(response, conversation_memory)


def extract_content(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    print(request_content)
    message = request_content['nlp']['source']
    conversation_memory = request_content['conversation']['memory']
    token= conversation_memory.get('token')
    channel = conversation_memory.get('channel')
    timestamp = request_content['nlp']['timestamp']
    return  channel, timestamp, message, token , conversation_memory


def call_dynalist_api(api_adress,dynalist_payload):
    r = requests.post(api_adress, json=dynalist_payload)
    return r


def build_recast_response(response_dynalist, conversation_memory):
    response_dynalist = response_dynalist.json()
    #print(response_dynalist)
    memory_response = conversation_memory
    memory_response['status_code'] = response_dynalist.get('_code', 'NoResponse')
    memory_response['status_message'] = response_dynalist.get('_msg', '')
    #print(memory_response)
    response_recast = jsonify(
        status=200,
        conversation={
            'memory': memory_response
        }
    )
    return response_recast


def build_dynalist_payload(dynalist_token, message, check_token_only, note):
    if check_token_only :
        dynalist_payload = {
            "token": dynalist_token
        }
    else:
        dynalist_payload = {
            "token": dynalist_token,
            "content": message,
            "note": note
        }
    return dynalist_payload



def build_dynalist_note(channel,contact, timestamp):
    if channel:
        dynalist_channel = '@' + channel
    else:
        dynalist_channel = '@' + 'channel'

    time = '!(' + timestamp + ')'

    if contact:
        contact = '@' + contact
    else:
        contact = '@' + 'AContact'

    return '#message on {0} from {1} {2}'.format(dynalist_channel,contact,time)
