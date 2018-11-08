# coding: utf-8

import os
import recastai
from flask import request
import requests

from flask import jsonify

#Custom libraries
import json


def post_to_inbox(payload):
    message, conversation_memory = extract_content(payload)
    payload = build_dynalist_payload(conversation_memory['token'], message)
    response = call_dynalist_api_inbox(payload)
    return build_recast_response(response, conversation_memory)

def check_token_request(payload):
    message, conversation_memory = extract_content(payload)
    payload = build_dynalist_payload(conversation_memory['token'], "")
    response = call_dynalist_api_inbox(payload)
    return build_recast_response(response, conversation_memory)


def extract_content(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    message = request_content['nlp']['source']
    conversation_memory = request_content['conversation']['memory']
    return  message, conversation_memory


def call_dynalist_api_inbox(dynalist_payload):
    r = requests.post('https://dynalist.io/api/v1/inbox/add', json=dynalist_payload)
    return r


def build_recast_response(response_dynalist, conversation_memory):
    response_dynalist = response_dynalist.json()
    print(response_dynalist)
    memory_response = conversation_memory
    memory_response['status_code'] = response_dynalist.get('_code', 'NoResponse')
    memory_response['status_message'] = response_dynalist.get('_msg', '')
    print(memory_response)
    response_recast = jsonify(
        status=200,
        conversation={
            'memory': memory_response
        }
    )
    return response_recast


def build_dynalist_payload(dynalist_token, message):
    dynalist_payload = {
        "token": dynalist_token,
        "index": 0,
        "content": message,
        "note": "",
        "checked": False
    }
    return dynalist_payload



