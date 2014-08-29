#!/usr/bin/env python

import utils

from speeches.utils.scraping import BaseParser
from speeches.models import Speaker, Speech

from conservative.scrape import get_speeches
from conservative.parse import parse_speech


class Parser(BaseParser):
    instance = 'party-speeches'

    def get_transcripts(self):
        return get_speeches()

    def parse(self, data):
        url, date, heading, speaker, text = data
        text, speaker = parse_speech(text, speaker)
        speaker = self.get_or_create(
            Speaker,
            instance=self.instance,
            name=speaker,
            )
        speech = Speech(
            instance=self.instance,
            text=text,
            speaker=speaker,
            start_date=date,
            heading=heading,
            source_url=url,
            type='speech',
            )
        if self.commit:
            speech.save()


parser = Parser(cache_dir=utils.CACHE_DIR)
parser.run()
