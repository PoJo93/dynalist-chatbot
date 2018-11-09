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
    return request_dynalist(payload, extract_content_inbox, 'https://dynalist.io/api/v1/inbox/add')

def check_token_request(payload ):
    print("Check TOken was activated")
    return request_dynalist(payload, extract_content_check_token, 'https://dynalist.io/api/v1/file/list')


def request_dynalist(payload, extraction_method, api_adress):
    message, token, conversation_memory = extraction_method(payload)
    payload = build_dynalist_payload(token, message)
    response = call_dynalist_api(api_adress, payload )
    return build_recast_response(response, conversation_memory)


def extract_content_inbox(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    message = request_content['nlp']['source']
    conversation_memory = request_content['conversation']['memory']
    token= conversation_memory.get('token')
    return  message, token , conversation_memory

def extract_content_check_token(payload):
    request_content = json.loads(payload.get_data().decode('utf-8'))
    message = ""
    conversation_memory = request_content['conversation']['memory']
    token= request_content['nlp']['entities']['dynalist-token'][0]['raw']
    return  message, token , conversation_memory

def call_dynalist_api(api_adress,dynalist_payload):
    r = requests.post(api_adress, json=dynalist_payload)
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
    if message is not "":
        dynalist_payload = {
            "token": dynalist_token,
            "content": message,
        }
    else:
        dynalist_payload = {
            "token": dynalist_token
        }
    return dynalist_payload



