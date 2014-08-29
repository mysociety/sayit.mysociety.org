#!/usr/bin/env python
from urlparse import urljoin

import utils

from speeches.utils.scraping import BaseParser
from speeches.models import Speaker, Speech

from labour.scrape import get_speeches
from labour.parse import parse_speech, ParsingError


class Parser(BaseParser):
    instance = 'party-speeches'

    index_url = 'http://www.labour.org.uk/news-archive'
    # If you want to start on a later page, the index url looks something
    # like this:
    # index_url = 'http://www.labour.org.uk/news-archive?c076b2da-a7a5-f434-9d91-aa2dc9db98cc=683'

    def get_transcripts(self):
        return get_speeches(self.index_url)

    def parse(self, data):
        url = data['url']
        soup = data['soup']

        try:
            text, name, image_url, date = parse_speech(soup)
        except ParsingError as e:
            print 'SKIPPING {} - {}'.format(url, e.args[0])
            return

        # If get_or_create in BaseParser supported defaults, and returned
        # a 'created' boolean in the usual way, this could be slightly neater
        speaker = self.get_or_create(
            Speaker,
            instance=self.instance,
            name=name,
            )
        if not speaker.image:
            speaker.image = urljoin(self.index_url, image_url)
        speaker.save()

        speech = Speech(
            instance=self.instance,
            text=text,
            speaker=speaker,
            start_date=date,
            title=data['title'],
            source_url=url,
            type='speech',
            )
        if self.commit:
            speech.save()


parser = Parser(cache_dir=utils.CACHE_DIR)
parser.run()
