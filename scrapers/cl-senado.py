#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import datetime
import re

import utils

from speeches.utils.scraping import BaseParser, ParserSpeech as Speech


class CLSenadoParser(BaseParser):
    instance = 'senado-de-chile'

    def get_transcripts(self):
        url = 'http://www.senado.cl/appsenado/index.php?mo=tramitacion&ac=getDiscusion&nrobol=618906_P&idsesion=7007'
        date = datetime.date(2014, 1, 21)
        yield {
            'url': url,
            'date': date,
            'text': self.get_url(url, 'html'),
        }

    def top_section_heading(self, data):
        text = data['text'].find('div', 'texto')
        heading = text.find('p').text.strip().title()
        heading = '%s, %s' % (heading, data['date'].strftime('%d-%m-%Y'))
        return heading

    def fix_name(self, name):
        name = name.title().replace('El S', 'El s').replace('La S', 'La s')
        return name

    def parse_transcript(self, data):
        print "PARSING %s" % data['url']

        text = data['text'].find('div', 'texto')

        # Sometimes, last paragraph of text isn't in a <p>
        for p in text('p')[1:]:
            if re.search('\S', unicode(p.next_sibling)):
                last_para = sib = p
                while sib.next_sibling and getattr(sib.next_sibling, 'name') != 'p':
                    sib = sib.next_sibling
                    if getattr(sib, 'name'): continue
                    new_para = data['text'].new_tag('p')
                    new_para.string = sib.strip()
                    last_para.insert_after(new_para)
                    last_para = new_para

        speech = None
        for p in text('p')[1:]:

            line = p.text.strip()

            # New speaker
            if '.-' in line:
                yield speech
                m = re.match(
                    u'((?:La señora|El señor) [^ ]*)( \([^)]*\))?\.-(.*)',
                    line)
                speaker = self.fix_name(m.group(1))
                speaker_display = None
                if m.group(2):
                    if '(don' in m.group(2):
                        speaker += m.group(2)
                    else:
                        speaker_display = speaker + m.group(2)
                speech = Speech(
                    speaker=speaker,
                    text=m.group(3).strip(),
                    speaker_display=speaker_display,
                    )
                continue

            # Narrative
            if re.match('--', line):
                yield speech
                speech = Speech(speaker=None, text=line)
                continue

            # We must now already have a speech by the time we're here
            if not speech:
                raise Exception, 'Reached here without a speech - need to deal with "%s"' % line.encode('utf-8')

            speech.add_para(line)

        yield speech

parser = CLSenadoParser(cache_dir=utils.CACHE_DIR)
parser.run()

