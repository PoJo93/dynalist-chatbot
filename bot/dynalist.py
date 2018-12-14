import requests
import typing

class DynalistClient:
    """This client handles the calls to the dynalist API enpoints"""

    def _call_api(self, recast_conversation, api):
        payload = api.build_api_request(self, recast_conversation=recast_conversation)
        print(payload)
        return requests.post(api.address, json=payload)

    def call_check_token_api(self, recast_conversation):
        return self._call_api(recast_conversation=recast_conversation, api=CheckTokenAPI)

    def call_inbox_add_api(self, recast_conversation):
        return self._call_api(recast_conversation=recast_conversation, api=InboxAddAPI)


class DynalistApiType:
    address = None

    def build_api_request (self, recast_conversation):
        pass

class CheckTokenAPI(DynalistApiType):
    address = 'https://dynalist.io/api/v1/file/list'

    def build_api_request(self, recast_conversation):
        return {"token": recast_conversation.token}

class InboxAddAPI(DynalistApiType):
    address = 'https://dynalist.io/api/v1/inbox/add'

    def build_api_request(self, recast_conversation):
        item = DynalistItem.from_recast_conversation(recast_conversation)
        return {
            "token": item.get_token(),
            "content": item.get_content(),
            "note": item.get_note()
        }



class DynalistItem:
    """Building together a note to write down metadata about the message"""

    @classmethod
    def from_recast_conversation(cls, response):
        return DynalistItem(response.channel, response.timestamp, response.contact, response.token, response.message)

    def __init__(self, channel: str, timestamp: str, contact: str, token: str, content: str):
        self.channel = channel
        self.timestamp = timestamp
        self.contact = contact
        self.token = token
        self.content = content
        self.note = ""

    def get_note(self):
        self.build_note()
        self.note

    def build_note(self):
        if self.channel:
            capitalized_channel_words = [x.capitalize() for x in self.channel.split()]
            capitalized_channel = ''.join(capitalized_channel_words)
            channel_str = '@' + capitalized_channel
        else:
            channel_str = '@' + 'channel'
        time_str = '!(' + self.timestamp + ')'
        if self.contact:
            contact_str = '@' + self.contact
        else:
            contact_str = '@' + 'AContact'
        self.note = '#message on {0} from {1} {2}'.format(channel_str, contact_str, time_str)

    def get_content(self):
        return self.content

    def get_token(self):
        return self.token






