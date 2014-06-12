#!/usr/bin/env python

import datetime
import os
import re
import urlparse
import urllib
import socket

import bs4

from utils import BaseParser, prevnext
from utils import ParserSpeech as Speech, ParserSection as Section

class PhilaParser(BaseParser):
    instance = 'philadelphia'

    def __init__(
        self,
        year,
        month=None, # None will represent all months
        day=None, # There is no point in setting day unless month is also set.
        index_url=None,
        committee_name=None,
        ):

        self.year = year

        if month:
            self.month = month
            self.day = '{0:02d}'.format(day) if day else 'ALL_DAYS'
        else:
            self.month = 'ALL MONTHS'
            self.day = None

        self.index_url = index_url
        self.committee_name = committee_name

        super(PhilaParser, self).__init__()

    def get_transcripts(self):
        get_resp = self.requests.get(self.index_url)

        soup = bs4.BeautifulSoup(get_resp.content)
        form = soup.find('form', id='Form1')

        # FIXME - don't cache the index page.
        post_data = {
            '__VIEWSTATE': form.find('input', id='__VIEWSTATE')['value'],
            '__EVENTVALIDATION': form.find('input', id='__EVENTVALIDATION')['value'],
            'Button3': 'submit',
            'ddlYear': self.year,
            'ddlMonth': self.month,
            }

        if self.committee_name:
            post_data['ddCommittee'] = self.committee_name

        if self.day:
            post_data['ddlDay'] = self.day

        resp = self.requests.post(self.index_url, data=post_data)

        soup = bs4.BeautifulSoup(resp.content)

        # I'm not really happy with this, but it seems like the least bad option
        # available for finding all these documents. Let's hope the text doesn't
        # change!
        trs = [x.find_parent('tr') for x in soup.findAll(text='Retrieve Document')]

        for tr in trs:
            tds = tr.findAll('td')

            date = datetime.datetime.strptime(
                tds[1].font.text.strip(), '%m/%d/%Y').date()
            url = urlparse.urljoin(self.index_url, tds[2].a['href'])
            try:
                text = self.get_pdf(url)
            except socket.error:
                print "SKIPPING {} - error downloading".format(url)
            else:
                yield {'date': date, 'url': url, 'text': text}

    def top_section_title(self, data):
        return 'Council meeting, %s' % data['date'].strftime('%d %B %Y').lstrip('0')

    def parse_transcript(self, data):
        print "PARSING %s" % data['url']

        page, num = 1, 1

        speech = None
        state = 'text'
        Speech.reset(True)

        for prev_line, line, next_line in prevnext(data['text']):
            # Page break
            if '\014' in line:
                page += 1
                num = 0
                continue

            if state == 'skip1':
                state = 'text'
                continue

            # Empty line, or line matching page footer
            if re.match('\s*$', line):
                continue
            if re.match(' *Strehlow & Associates, Inc.$| *\(215\) 504-4622$', line):
                continue

            # Ignore title page for now
            if page == 1:
                continue

            # Start of certificate/index
            if re.match(
                ' *\d+ *(CERTIFICATE|C E R T I F I C A T I O N|- - -)$', line):
                state = 'index'
            if state == 'index':
                continue

            # Each page starts with page number
            if num == 0:
                m = re.match(' +(\d+)$', line)
                assert int(m.group(1)) == page
                num += 1
                continue

            # Heading somewhere within this page, just ignore it
            if num == 1:
                num += 1
                continue

            # Let's check we haven't lost a line anywhere...
            assert re.match(' *%d(   |$)' % num, line), '%s != %s' % (num, line)
            line = re.sub('^ *%d(   |$)' % num, '', line)
            num += 1

            # Narrative messages
            m = re.match(' +(\(.*\))$', line)
            if m:
                yield speech
                speech = Speech( speaker=None, text=line )
                continue
            m1 = re.match(' +(\(.*)$', line)
            m2 = re.match(' *\d+ +(.*\))$', next_line)
            if m1 and m2:
                yield speech
                speech = Speech( speaker=None, text='%s %s' % (m1.group(1), m2.group(1)) )
                state = 'skip1'
                num += 1
                continue

            # Okay, here we have a non-empty, non-page number, non-narrative line of just text
            # print page, num, line

            # New speaker
            m = re.match(" *([A-Z '.]+):(?: (.*)|$)", line)
            if m:
                yield speech
                speaker = self.fix_name(m.group(1))
                text = m.group(2) or ''
                speech = Speech( speaker=speaker, text=text )
                continue

            # We must now already have a speech by the time we're here
            if not speech:
                raise Exception, 'Reached here without a speech - need to deal with "%s"' % line

            if re.match(' ', line):
                speech.add_para(line.strip())
            else:
                speech.add_text(line.strip())

        yield speech


parser = PhilaParser(
    2013,
    index_url='http://legislation.phila.gov/council-transcriptroom/transroom_date.aspx',
    )
parser.run()

