#!/usr/bin/env python

import utils

from speeches.utils.scraping import BaseParser
from speeches.models import Speaker, Speech

from labour.scrape import get_speeches
from labour.parse import parse_speech, ParsingError


class Parser(BaseParser):
    instance = 'old-labour-speeches'

    def get_transcripts(self):
        return get_speeches()

    def parse(self, data):
        url = data['url']
        soup = data['soup']

        try:
            text, name, date = parse_speech(soup)
        except ParsingError as e:
            print 'SKIPPING {} - {}'.format(url, e.args[0])
            return

        speaker = self.get_or_create(
            Speaker,
            instance=self.instance,
            name=name,
            )
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
