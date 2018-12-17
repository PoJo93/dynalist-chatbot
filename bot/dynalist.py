import requests
import typing
from bot import Entity
from bot import RecastConversation

class DynalistClient:
    """This client handles the calls to the dynalist API enpoints"""

    def _call_api(self, recast_conversation, api):
        payload = api.build_api_request(self, conversation=recast_conversation)
        print(payload)
        return requests.post(api.address, json=payload)

    def call_check_token_api(self, recast_conversation):
        return self._call_api(recast_conversation=recast_conversation, api=CheckTokenAPI)

    def call_inbox_add_api(self, recast_conversation):
        return self._call_api(recast_conversation=recast_conversation, api=InboxAddAPI)


class DynalistApiType:
    address = None

    def build_api_request (self, conversation: RecastConversation):
        pass


class CheckTokenAPI(DynalistApiType):
    address = 'https://dynalist.io/api/v1/file/list'

    def build_api_request(self, conversation: RecastConversation):
        return {"token": conversation.token}


class InboxAddAPI(DynalistApiType):
    address = 'https://dynalist.io/api/v1/inbox/add'

    def build_api_request(self, conversation: RecastConversation):
        item = DynalistItem.from_recast_conversation(conversation)

        map_entities = {
            'person': item.format_person,
            'datetime': item.format_datetime,
            'location': item.format_location,
            'email': item.format_email
        }

        for entity in conversation.entities:
            processing_method = map_entities.get(entity.name)
            if processing_method:
                processing_method(entity)

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
        return self.note

    def build_note(self):
        if self.channel:
            channel_str = self.to_add_tag(self.channel)
        else:
            channel_str = '@' + 'channel'
        time_str = '!(' + self.timestamp + ')'
        if not self.contact:
            contact_str = '@' + 'AContact'
        else:
            contact_str = self.contact

        self.note = '#message on {0} from {1} {2}'.format(channel_str, contact_str, time_str)

    def get_content(self):
        return self.content

    def get_token(self):
        return self.token

    def format_person(self, entity: Entity):
        if entity.name == 'person':
            formatted_name = self.to_add_tag(entity.fullname)
            pattern_whatsapp= '[{0}] '
            pattern_custom = ' @ {0}'
            if not self.replace_contact(entity.raw, pattern_whatsapp, formatted_name):
                if not self.replace_contact(entity.raw, pattern_custom, formatted_name):
                    self.content = self.content.replace(entity.raw, formatted_name)

    def format_datetime(self, entity: Entity):
        if entity.name == 'datetime':
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
            closest_accuracy = entity.accuracy.rpartition(',')[2]
            formatted_date = entity.iso[:accuracy_dict[closest_accuracy]]
            dynalist_formatted_date = ' (!({0}))'.format(formatted_date)
            self.content = (entity.raw + dynalist_formatted_date).join(self.content.split(entity.raw))

    def format_location(self, entity: Entity):
        if entity.name == 'location':
            google_url = 'https://www.google.com/maps/place/?q=place_id:' + entity.place
            self.insert_link_in_content(google_url, entity.raw)

    def format_email(self, entity: Entity):
        mail_url = 'mailto:' + entity.raw
        self.insert_link_in_content(mail_url, entity.raw)

    def insert_link_in_content(self, url: str, raw: str):
        link_format = '[{0}]({1})'
        self.content = (link_format.format(raw, url)).join(self.content.split(raw))

    # TODO move to utils
    def to_add_tag(self, tag: str):
        capitalized_words = [x.capitalize() for x in tag.split()]
        capitalized_word = ''.join(capitalized_words)
        channel_str = '@' + capitalized_word
        return channel_str

    def replace_contact (self, raw_name: str, pattern: str, name: str):
        if pattern.format(raw_name) in self.content:
            self.content = self.content.replace(pattern.format(raw_name), '')
            self.contact = name
            return True
        return False






