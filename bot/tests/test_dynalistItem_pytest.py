import pytest
from bot import DynalistItem
from bot import Entity

def my_dynalist_item(content):
    return DynalistItem(channel='Telegram', timestamp='', contact='', token=None,
                        content=content)


def test_format_person_custom():
    item =my_dynalist_item(content='Hey can you sign this form for me? @ jonathan schneider')
    person_entity = Entity('person', {
        "fullname": "jonathan schneider",
        "raw": "jonathan schneider",
        "confidence": 0.99
      })

    item.format_person(person_entity)
    assert 'Hey can you sign this form for me?' == item.content
    assert '@JonathanSchneider' == item.contact


def test_format_person_whatsapp():
    item = my_dynalist_item(content='[Jonathan Schneider] Hey can you sign this form for me?')
    person_entity = Entity('person', {
        "fullname": "Jonathan Schneider",
        "raw": "Jonathan Schneider",
        "confidence": 0.99
      })
    item.format_person(person_entity)
    assert 'Hey can you sign this form for me?' == item.content
    assert '@JonathanSchneider' == item.contact


def test_format_person_normal():
    item = my_dynalist_item(content='Can you tell leonardo to get it done ASAP?')
    person_entity = Entity('person', {
        "fullname": "leonardo",
        "raw": "leonardo",
        "confidence": 0.96
      })
    item.format_person(person_entity)
    assert 'Can you tell @Leonardo to get it done ASAP?' == item.content
    assert '' == item.contact


def test_format_datetime_day():
    item = my_dynalist_item(content='Hey Jonas can we meet tomorrow in the bar')
    date_entity = Entity('datetime', {
        "formatted": "Tuesday, 18 December 2018 at 02:05:45 PM (+0000)",
        "iso": "2018-12-18T14:05:45+00:00",
        "accuracy": "day",
        "chronology": "future",
        "state": "relative",
        "raw": "tomorrow",
        "confidence": 0.99
      }
    )

    item.format_datetime(date_entity)
    assert 'Hey Jonas can we meet tomorrow (!(2018-12-18)) in the bar' == item.content


def test_format_datetime_time():
    item = my_dynalist_item(content='Hey Jonas can we meet tomorrow at 1pm in the bar')
    date_entity = Entity('datetime', {
        "formatted": "Tuesday, 18 December 2018 at 01:00:00 PM (+0000)",
        "iso": "2018-12-18T13:00:00+00:00",
        "accuracy": "day,halfday,hour,min",
        "chronology": "future",
        "state": "relative",
        "raw": "tomorrow at 1pm",
        "confidence": 0.95
      })
    item.format_datetime(date_entity)
    assert 'Hey Jonas can we meet tomorrow at 1pm (!(2018-12-18T13:00)) in the bar' == item.content


def test_format_location():
    item = my_dynalist_item(content='Meet me at SAP in 3475 Deer Creek Road')
    location_entity = Entity('location', {
        "formatted": "3475 Deer Creek Rd, Palo Alto, CA 94304, USA",
        "lat": 37.3956331,
        "lng": -122.1487259,
        "type": "street_address",
        "place": "ChIJwwPne3Wwj4AROzUKSvci2Hw",
        "raw": "3475 Deer Creek Road",
        "confidence": 0.65,
        "country": "us"
      })
    item.format_location(location_entity)
    assert 'Meet me at SAP in [3475 Deer Creek Road]' \
           '(https://www.google.com/maps/place/?q=place_id:ChIJwwPne3Wwj4AROzUKSvci2Hw)' == item.content


def test_format_email():
    item = my_dynalist_item('Hey please message someone@example.com for the meeting')
    email_entity = Entity('location', {
        "local": "someone",
        "tag": None,
        "domain": "example.com",
        "raw": "someone@example.com",
        "confidence": 0.99
      })
    item.format_email(email_entity)
    assert 'Hey please message [someone@example.com](mailto:someone@example.com) for the meeting' == item.content

def test_format_phone_international():
    item = my_dynalist_item('Hey call me on +12025550159')
    email_entity = Entity('phone', {
        "number": "+12025550159",
        "raw": "+12025550159",
        "confidence": 0.99
      })
    item.format_phone(email_entity)
    assert 'Hey call me on [🇺🇸 +1 202-555-0159](tel:+12025550159)' == item.content

def test_format_phone_national_US():
    item = my_dynalist_item('Hey call me on 2025550159')
    email_entity = Entity('phone', {
        "number": "2025550159",
        "raw": "2025550159",
        "confidence": 0.99
      })
    item.format_phone(email_entity)
    assert 'Hey call me on [(202) 555-0159](tel:2025550159)' == item.content