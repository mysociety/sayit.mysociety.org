#!/usr/bin/env python

import utils

from speeches.utils.scraping import BaseParser

from leveson.scrape import get_transcripts
from leveson.parse import parse_transcript


class LevesonParser(BaseParser):
    instance = 'leveson'

    def skip_transcript(self, data):
        if '2011-11-21pm' in data['url']: return True # Included in the morning
        if '2011-12-15am' in data['url']: return True # Included in the afternoon
        return False

    def get_transcripts(self):
        return get_transcripts(self.cache_dir)

    def parse_transcript(self, data):
        return parse_transcript(data['text'], data['url'])


parser = LevesonParser(cache_dir=utils.CACHE_DIR)
parser.run()
