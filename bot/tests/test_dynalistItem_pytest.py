import pytest
from bot import DynalistItem


def my_dynalist_item(content):
    return DynalistItem(channel='Telegram', timestamp='', contact='', token=None,
                        content=content)


def test_format_person_custom():
    item =my_dynalist_item(content='Hey can you sign this form for me? @ jonathan schneider')
    item.format_person("jonathan schneider", "jonathan schneider", 0.99)
    assert 'Hey can you sign this form for me?' == item.content
    assert '@JonathanSchneider' == item.contact

def test_format_person_whatsapp():
    item = my_dynalist_item(content='[Jonathan Schneider] Hey can you sign this form for me?')
    item.format_person("Jonathan Schneider", "Jonathan Schneider", 0.99)
    assert 'Hey can you sign this form for me?' == item.content
    assert '@JonathanSchneider' == item.contact

def test_format_person_normal():
    item = my_dynalist_item(content='Can you tell leonardo to get it done ASAP?')
    item.format_person("leonardo", "leonardo", 0.96)
    assert 'Can you tell @Leonardo to get it done ASAP?' == item.content
    assert '' == item.contact

