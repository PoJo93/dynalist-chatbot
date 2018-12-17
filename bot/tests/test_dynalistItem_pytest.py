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


def test_format_datetime_day():
    item = my_dynalist_item(content='Hey Jonas can we meet tomorrow in the bar')
    item.format_datetime(_formatted='Tuesday, 18 December 2018 at 11:38:59 AM (+0000)',
                         iso='2018-12-18T11:38:59+00:00',
                         accuracy="day",
                         _chronology="future",
                         _state="relative",
                         raw='tomorrow',
                         _confidence=0.99)
    assert 'Hey Jonas can we meet tomorrow (!(2018-12-18)) in the bar' == item.content


def test_format_datetime_time():
    item = my_dynalist_item(content='Hey Jonas can we meet tomorrow at 1pm in the bar')
    item.format_datetime(formatted='Tuesday, 18 December 2018 at 01:00:00 PM (+0000)',
                         iso='2018-12-18T13:00:00+00:00',
                         accuracy="day,halfday,hour,min",
                         chronology="future",
                         state="relative",
                         raw='tomorrow at 1pm',
                         confidence=0.95)
    assert 'Hey Jonas can we meet tomorrow at 1pm (!(2018-12-18T13:00)) in the bar' == item.content


def test_format_location():
    item = my_dynalist_item(content='Meet me at SAP in 3475 Deer Creek Road')
    item.format_location(formatted="3475 Deer Creek Rd, Palo Alto, CA 94304, USA",
                         lat=37.3956331,
                         lng=-122.1487259,
                         type="street_address",
                         place="ChIJwwPne3Wwj4AROzUKSvci2Hw",
                         raw="3475 Deer Creek Road",
                         confidence=0.65,
                         country="us")
    assert 'Meet me at SAP in [3475 Deer Creek Road]' \
           '(https://www.google.com/maps/place/?q=place_id:ChIJwwPne3Wwj4AROzUKSvci2Hw)' == item.content


def test_format_email():
    item = my_dynalist_item('Hey please message someone@example.com for the meeting')
    item.format_email(local='someone',
                      tag=None,
                      domain="example.com",
                      raw="someone@example.com",
                      confidence=0.99)
    assert 'Hey please message [someone@example.com](mailto:someone@example.com) for the meeting' == item.content
