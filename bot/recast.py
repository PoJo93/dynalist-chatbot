
from flask import jsonify


def build_response(recast_conversation, dynalist_response):
    dynalist_response_json = dynalist_response.json()
    memory_response = recast_conversation.conversation_memory
    memory_response['status_code'] = dynalist_response_json.get('_code', 'NoResponse')
    memory_response['status_message'] = dynalist_response_json.get('_msg', '')
    response = jsonify(
        status=200,
        conversation={
            'memory': memory_response
        }
    )
    return response


class RecastConversation:
    """"Encapsulates the relevant attributes from a recast conversation"""

    @classmethod
    def from_json_payload(cls, payload: dict):
        print(payload)
        message = payload['nlp']['source']
        conversation_memory = payload['conversation']['memory']
        token = conversation_memory.get('token')
        channel = conversation_memory.get('channel')
        timestamp = payload['nlp']['timestamp']
        entities = payload['entities']
        contact = conversation_memory.get('contact')
        return RecastConversation(message=message,
                                  conversation_memory=conversation_memory,
                                  token=token,
                                  channel=channel,
                                  timestamp=timestamp,
                                  contact=contact,
                                  entities=entities)

    def __init__(self, message: str, conversation_memory: str, token: str, channel: str, timestamp: str, contact: str, entities):
        self.message = message
        self.conversation_memory = conversation_memory
        self.token = token
        self.channel = channel
        self.timestamp = timestamp
        self.contact = contact
        self.entities = [Entity(n, ee) for n, e in entities.items() for ee in e]





class Entity():
  def __init__(self, name, entity):
    self.name = name

    for k, v in entity.items():
      setattr(self, k, v)

  def __repr__(self):
    attributes = []
    for method in dir(self):
      if not method.startswith('__') and method != 'name':
        value = getattr(self, method)
        attributes.append("{}={}".format(method, value))

    return "{} ({})".format(self.name, ', '.join(attributes))
