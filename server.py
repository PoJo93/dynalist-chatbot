#coding: utf-8

import os, json

from flask import Flask, request
from bot import cai, dynalist


port = int(os.getenv("PORT"))
app = Flask(__name__)
dynalist_client = dynalist.DynalistClient()

@app.route("/post_to_inbox", methods=['POST'])
def post_to_inbox():
    return process_request(request, dynalist_client.call_inbox_add_api)


# GET would be semantically the better option but doesn't work here as we have to submit a JSON payload
@app.route("/auth/validate", methods=['POST'])
def validate_token():
    return process_request(request, dynalist_client.call_check_token_api)

@app.route("/dialogflow/test", methods=['POST'])
def debug_dialogflow():
    request_json =json.loads(request.get_data().decode('utf-8'))
    print(json.dumps(request_json, indent=5, sort_keys=False))

def process_request(request_cai, clientApiMethod):
    cai_json = json.loads(request_cai.get_data().decode('utf-8'))
    cai_conversation = cai.CAIConversation.from_json_payload(cai_json)

    response = clientApiMethod(cai_conversation)
    return cai.build_response(cai_conversation, response)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port)

