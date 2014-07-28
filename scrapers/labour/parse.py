from datetime import datetime
from bs4 import Comment


class ParsingError(Exception):
    pass

skip_names = set([
    'Independent Commission - Police',
    'children',
    'Tory failure receipt',
    'rose30',
    'Poster 2',
    'labour rose',
    'Labour Rose',
    'Rose',
    ])

name_corrections = {
    'EdV2': 'Ed Miliband',
    'Ed Miliband04/08': 'Ed Miliband',
    'Ed_LOU': 'Ed Miliband',
    'Ed_LOU1': 'Ed Miliband',
    'ed_miliband_speech': 'Ed Miliband',
    'edm': 'Ed Miliband',
    'Rob_Flello1': 'Rob Flello',
    'Robert Flello': 'Rob Flello',
    'John_Healey_use': 'John Healey',
    'Healey': 'John Healey',
    'Hanson': 'David Hanson',
    'hid': 'Huw Irranca-Davies',
    'Catherine McKinnell 2': 'Catherine McKinnell',
    'Catherine McKinnell 1': 'Catherine McKinnell',
    'Kevan_Jones': 'Kevan Jones',
    'owen_smith': 'Owen Smith',
    'Jenny_Chapman': 'Jenny Chapman',
    'Ann Mc': 'Ann McKechin',
    'Anne Mc': 'Ann McKechin',
    'ken': 'Ken Livingstone',
    'Clive_Efford': 'Clive Efford',
    'Gemma_Doyle': 'Gemma Doyle',
    'Diana Johnson MP': 'Diana Johnson',
    'Steve Rotheram1': 'Steve Rotheram',
    'Gloria': 'Gloria De Piero',
    'Angela Eagle MP': 'Angela Eagle',
    'Angela Smith MP': 'Angela Smith',
    'ann at labour': 'Ed Miliband',
    'iain': 'Iain McNicol',
    }


def normalize_speaker_name(name):
    name = name.strip()
    if name in skip_names:
        raise ParsingError('Skipping article with name: {}'.format(name))

    name = name_corrections.get(name, name)
    if name.islower():
        name = name.title()
    return name


def parse_speech(soup):
    speech = (soup.find('div', {'class': 'post-wrapper'}) or
              soup.find('div', {'class': 'articles-alt'}))

    if not speech:
        raise ParsingError('Speech fragment not found')
    speech.extract()

    date_element = speech.find('span', {'class': 'date'})

    if date_element:
        date = datetime.strptime(date_element.text.strip(), '%d %B %Y')
        date_element.extract()
    else:
        date = None

    img_element = speech.img
    if img_element:
        speaker_name = normalize_speaker_name(img_element['alt'])
        image_url = img_element['src']
        img_element.extract()
    else:
        raise ParsingError('No img found - used for speaker name')

    # Remove some stuff from the speech that we don't need:
    # comments - the heading, if it's there, and social sharing stuff.
    [x.extract() for x in
     speech.findAll(text=lambda text:isinstance(text, Comment))]
    [x.extract() for x in speech.findAll('h2')]
    [x.extract() for x in speech.findAll('div', {'class': 'social-share'})]

    # Change these tags to things allowed in Akoma Ntoso
    for tag in speech.findAll('strong'):
        tag.name = 'b'
    for tag in speech.findAll('em'):
        tag.name = 'i'

    text = (u'\n'.join([unicode(x) for x in speech.contents if x])).strip()

    return text, speaker_name, image_url, date
