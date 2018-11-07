#coding: utf-8

import os
import config

from flask import Flask, request
from bot import post_to_inbox, check_token_request


app = Flask(__name__)

@app.route("/post_to_inbox", methods=['POST'])
def post_to_inbox_route():
  return post_to_inbox(request)

@app.route("/check_token", methods=['POST'])
def check_token_route():
  return check_token_request(request)

#app.run(port=os.environ['PORT'])
app.run(port=5000)
