from datetime import datetime
from bs4 import Comment


class ParsingError(Exception):
    pass


def normalize_speaker_name(name):
    return name

def parse_speech(soup):
    speech = soup.find('div', {'class': 'post-wrapper'})

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
        img_element.extract()
    else:
        raise ParsingError('No img found - used for speaker name')

    # Remove comments from the speech fragment
    [x.extract() for x in
     speech.findAll(text=lambda text:isinstance(text, Comment))]
    speech.find('h2').extract()
    speech.find('div', {'class': 'social-share'}).extract()

    # Change these tags to things allowed in Akoma Ntoso
    for tag in speech.findAll('strong'):
        tag.name = 'b'
    for tag in speech.findAll('em'):
        tag.name = 'i'

    text = (u'\n'.join([unicode(x) for x in speech.contents if x])).strip()

    return text, speaker_name, date
