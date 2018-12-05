#coding: utf-8

import os, json

from flask import Flask, request
from bot import recast, dynalist


port = int(os.getenv("PORT"))
app = Flask(__name__)
dynalist_client = dynalist.DynalistClient()

@app.route("/post_to_inbox", methods=['POST'])
def post_to_inbox():
    return process_request(request, dynalist_client.call_inbox_add_api)


# TODO add comment why not get
@app.route("/auth/validate", methods=['POST'])
def validate_token():
    return process_request(request, dynalist_client.call_check_token_api)

def process_request(request_recast, clientApiMethod):
    recast_json = json.loads(request_recast.get_data().decode('utf-8'))
    recast_conversation = recast.RecastConversation.from_json_payload(recast_json)
    response = clientApiMethod(recast_conversation)
    return recast.build_response(recast_conversation, response)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port)

