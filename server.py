#coding: utf-8

import os

from flask import Flask, request
from bot import post_to_inbox, check_token_request

port = int(os.getenv("PORT"))

app = Flask(__name__)

@app.route("/post_to_inbox", methods=['POST'])
def post_to_inbox_route():
  return post_to_inbox(request)

@app.route("/check_token", methods=['POST'])
def check_token_route():
  return check_token_request(request)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port)

