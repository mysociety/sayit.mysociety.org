#!/usr/bin/env python

import os

import requests_cache

import utils

from speeches.utils.scraping import BaseParser, prevnext
from speeches.models import Speaker, Speech

from conservative.scrape import get_speeches
from conservative.parse import parse_speech


class Parser(BaseParser):
    instance = 'old-conservative-speeches'

    def get_transcripts(self):
        return get_speeches()

    def parse(self, data):
        url, date, title, speaker, text = data
        text, speaker = parse_speech(text, speaker)
        speaker = self.get_or_create(Speaker, instance=self.instance, name=speaker)
        speech = Speech(instance=self.instance, text=text, speaker=speaker, start_date=date, title=title, source_url=url)
        if self.commit:
            speech.save()


parser = Parser(cache_dir=utils.CACHE_DIR)
parser.run()
