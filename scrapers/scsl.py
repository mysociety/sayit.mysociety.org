#!/usr/bin/env python

from datetime import datetime

import os
import re

import requests_cache

import utils

from scsl.parse import parse_transcript
from speeches.utils.scraping import BaseParser


class SCSLParser(BaseParser):
    instance = 'charles-taylor'

    def __init__(self, *args, **kwargs):
        super(SCSLParser, self).__init__(*args, **kwargs)

        self.session_day = requests_cache.core.CachedSession(
            self.cache_dir, expire_after=86400)

    def skip_transcript(self, data):
        if data['date'].isoformat() == '2006-07-21': return True # Is garbled
        return False

    def get_transcripts(self):
        old_requests = self.requests
        self.requests = self.session_day
        transcripts = self.get_url('http://www.sc-sl.org/CASES/ProsecutorvsCharlesTaylor/Transcripts/tabid/160/Default.aspx', 'html')
        self.requests = old_requests
        # Loop through the rows in reverse order (so oldest first)
        for row in transcripts('p'):
            for thing in row.findAll(text=re.compile('\d')):
                text = thing.strip()
                if re.match('\d+$', text):
                    link = thing.find_parent('a')
                    date = date.replace(day=int(text))
                    url = link['href'].replace(' ', '%2B').replace('+', '%2B')

                    if 'tabid/160/www.sc-sl.org' in url:
                        url = re.sub('.*www', 'www', url)
                    if url[0:3] == 'www':
                        url = 'http://%s' % url
                    if url[0] == '/':
                        url = 'http://www.sc-sl.org' + url

                    # Wrong date on index page
                    if date.isoformat() == '2009-06-09':
                        date = date.replace(day=8)

                    yield {
                        'date': date,
                        'url': url,
                        'text': self.get_pdf(url, name=date.isoformat()+'.pdf'),
                    }

                else:
                    date = datetime.strptime(thing, '%B %Y').date()

    def parse_transcript(self, data):
        return parse_transcript(data['text'], data['date'])

    def prettify(self, s):
        s = s.title()
        s = s.replace('Dct-', 'DCT-').replace('Tfi-', 'TF1-').replace('Tf1-', 'TF1-')
        return s

parser = SCSLParser(cache_dir=utils.CACHE_DIR)
parser.run()
