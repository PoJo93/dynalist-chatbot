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
            channel_str = self.to_add_tag(self.channel)
        else:
            channel_str = '@' + 'channel'
        time_str = '!(' + self.timestamp + ')'
        if self.contact is '':
            contact_str = '@' + 'AContact'

        self.note = '#message on {0} from {1} {2}'.format(channel_str, contact_str, time_str)




    def get_content(self):
        return self.content

    def get_token(self):
        return self.token

    def format_person(self, fullname: str, raw: str, confidence: float):
        formatted_name = self.to_add_tag(fullname)

        pattern_whatsapp= '[{0}] '
        pattern_custom = ' @ {0}'

        if not self.replace_contact(raw, pattern_whatsapp, formatted_name):
           if not self.replace_contact(raw, pattern_custom, formatted_name):
               self.content = self.content.replace(raw, formatted_name)

    def format_datetime(self,
                        formatted: str,
                        iso: str,
                        accuracy: str,
                        chronology: str,
                        state: str,
                        raw: str,
                        confidence: float):

        # return cuttoff index from iso
        accuracy_dict = {
                        'year': 4,
                        'month': 7,
                        'week': 7,
                        'day': 10,
                        'halfday': 10,
                        'hour': 13,
                        'min': 16,
                        'sec': 19,
                        'now': 19
        }
        closest_accuracy = accuracy.rpartition(',')[2]
        formatted_date = iso[:accuracy_dict[closest_accuracy]]
        dynalist_formatted_date = ' (!({0}))'.format(formatted_date)
        self.content = (raw + dynalist_formatted_date).join(self.content.split(raw))

    def format_location(self,
                        formatted: str,
                        lat: float,
                        lng: float,
                        place: str,
                        type: str,
                        country: str,
                        raw: str,
                        confidence: float):
        google_url = 'https://www.google.com/maps/place/?q=place_id:' + place
        self.insert_link_in_content(google_url, raw)



    def format_email(self,
                     local: str,
                     tag: str,
                     domain: str,
                     raw: str,
                     confidence: float):
        mail_url = 'mailto:' + raw
        self.insert_link_in_content(mail_url, raw)



    def insert_link_in_content(self, url, raw):
        link_format = '[{0}]({1})'
        self.content = (link_format.format(raw, url)).join(self.content.split(raw))

    # TODO move to utils
    def to_add_tag(self, str):
        capitalized_words = [x.capitalize() for x in str.split()]
        capitalized_word = ''.join(capitalized_words)
        channel_str = '@' + capitalized_word
        return channel_str

    def replace_contact (self, raw_name, pattern, name):
        if pattern.format(raw_name) in self.content:
            self.content = self.content.replace(pattern.format(raw_name), '')
            self.contact = name
            return True
        return False






