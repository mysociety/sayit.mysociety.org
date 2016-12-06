#!/usr/bin/env python

import re

import utils

from speeches.utils.scraping import BaseParser

from brexit.scrape import get_transcripts
from brexit.parse import parse_transcript


class BrexitParser(BaseParser):
    instance = 'supreme-court-article-50-appeal'

    def skip_transcript(self, data):
        return False

    def get_transcripts(self):
        return get_transcripts(self.cache_dir)

    def parse_transcript(self, data):
        paras = {}
        for page, num, line in parse_transcript(data['text'], data['url']):
            line = re.sub('^( *).*', r'\1', line)
            paras.setdefault(page, {}).setdefault(len(line), 0)
            paras[page][len(line)] += 1
        para_min_indent = {}
        for page, lines in paras.items():
            para_min_indent[page] = min(lines) + 2

        return parse_transcript(data['text'], data['url'], para_min_indent=para_min_indent)


parser = BrexitParser(cache_dir=utils.CACHE_DIR)
parser.run()
