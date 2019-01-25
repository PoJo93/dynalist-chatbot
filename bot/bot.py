# coding: utf-8

from flask import jsonify
#Custom libraries


# both functions are doing the same on a different route
# create an DynalistClient class that encapsulates the Dynalist API
from bot.dynalist import call_dynalist_api, build_dynalist_note, build_dynalist_payload
from bot.cai import extract_content


def post_to_inbox(payload):
    print("inbox was activated")
    # use keyword arguments instead of unnamed flags
    # extract base URL and endpoint paths
    return request_dynalist(payload, 'https://dynalist.io/api/v1/inbox/add', False)

def check_token_request(payload ):
    print("Check TOken was activated")
    return request_dynalist(payload, 'https://dynalist.io/api/v1/file/list', True)


def request_dynalist(payload, api_adress, check_token_only):
    channel, timestamp, message, token, conversation_memory = extract_content(payload)
    note = build_dynalist_note(channel=channel, contact=None, timestamp=timestamp)
    payload = build_dynalist_payload(token, message, check_token_only, note)
    response = call_dynalist_api(api_adress, payload)
    return build_cai_response(response, conversation_memory)


def build_cai_response(response_dynalist, conversation_memory):
    response_dynalist = response_dynalist.json()
    #print(response_dynalist)
    memory_response = conversation_memory
    memory_response['status_code'] = response_dynalist.get('_code', 'NoResponse')
    memory_response['status_message'] = response_dynalist.get('_msg', '')
    #print(memory_response)
    response_cai = jsonify(
        status=200,
        conversation={
            'memory': memory_response
        }
    )
    return response_cai



