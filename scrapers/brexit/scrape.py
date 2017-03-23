#!/usr/bin/env python

import  datetime
import os
import re
import subprocess

import bs4

import utils
import requests
import requests_cache
requests_cache.install_cache(os.path.join(utils.CACHE_DIR, 'brexit'))

def get_url(url, type='none'):
    """Fetches a URL, and returns either its text, soup or content."""
    resp = requests.get(url)
    if type == 'binary':
        return resp.content
    elif type == 'html':
        return bs4.BeautifulSoup(resp.text)
    return resp.text

def convert_four_up_pdf(text):
    # Remove header/footer from all pages
    text = re.sub('\014?Day \d +Article 50 - Brexit Hearing +\d December 2016', '', text)
    text = re.sub('\(\+44\) *207 *404 *1400 +London EC4A 2DY', '', text)
    text = re.sub('DTI +www.DTIGlobal.com +8th Floor,? 165 Fleet Street', '', text)
    text = re.sub(' *\d+ \(Pages \d+ to \d+\)', '', text)
    text = re.sub('\xef\xbf\xbd', '', text)

    # Loop through, slurping up the pages by page number
    text_l, text_r = [], []
    pages = {}
    text = re.split('\r?\n', text)
    state = 'okay'
    for line in text:
        if re.match('\s*$', line): continue
        if re.match(r' +(\d+) .*? +\1 .*INDEX$', line): state = 'index'
        elif 'INDEX' in line: break

        m = re.match(r' +Page (\d+)(?: +Page (\d+))?', line)
        if m:
            page_l = int(m.group(1))
            pages[page_l] = text_l
            if m.group(2) and len(text_r):
                page_r = int(m.group(2))
                pages[page_r] = text_r
            text_l, text_r = [], []
            if state == 'index':
                break
            continue

        # Left and right pages
        m = re.match(r' +(\d+)( .*?) {2,}\1(  .*)?$', line)
        if m:
            line_n = int(m.group(1))
            line_l = '       %s' % m.group(2).rstrip()
            line_r = '       %s' % m.group(3) if m.group(3) else ''
            text_l.append('%2d%s' % (line_n, line_l))
            if state != 'index':
                text_r.append('%2d%s' % (line_n, line_r))
            continue
        # Just left page at the end
        m = re.match(r' +(\d+)( .*)?$', line)
        line_n = int(m.group(1))
        line_l = '       %s' % m.group(2) if m.group(2) else ''
        text_l.append('%2d%s' % (line_n, line_l))

    # Reconstruct in page order for normal processing
    text = ''
    for num, page in sorted(pages.items()):
        for line in page:
            text += line + '\n'
        text += '    %d\n\014\n' % num
    return text

def convert_pdf_transcript(url, cache_dir):
    file_pdf = os.path.join(cache_dir, os.path.basename(url))
    file_text = file_pdf.replace('.pdf', '.txt')
    if not os.path.exists(file_text):
        pdf_transcript = get_url(url, 'binary')
        fp = open(file_pdf, 'w')
        fp.write(pdf_transcript)
        fp.close()
        subprocess.call([ 'pdftotext', '-layout', file_pdf ])
        file_patch = file_pdf.replace('.pdf', '.patch')
        if os.path.exists(file_patch):
            inn = open(file_patch)
            subprocess.call([ 'patch', '--backup', file_text ], stdin=inn)
            inn.close()
    text = open(file_text).read()

    if 'four-page.pdf' in url:
        text = convert_four_up_pdf(text)

    # Be sure to have ^L on its own line
    text = text.replace('\014', '\014\n')

    return text

def get_transcript(url, cache_dir):
    text = convert_pdf_transcript(url, cache_dir)
    return re.split('\r?\n', text)

def get_transcripts(cache_dir):
    data = (
        (datetime.date(2016, 12, 5), 'https://www.supremecourt.uk/docs/draft-transcript-monday-161205-four-page.pdf'),
        (datetime.date(2016, 12, 6), 'https://www.supremecourt.uk/docs/draft-transcript-tuesday-161206.pdf'),
        (datetime.date(2016, 12, 7), 'https://www.supremecourt.uk/docs/draft-transcript-wednesday-161207.pdf'),
        (datetime.date(2016, 12, 8), 'https://www.supremecourt.uk/docs/draft-transcript-thursday-161208.pdf'),
    )
    for date, url in data:
        yield {
            'date': date,
            'url': url,
            'text': get_transcript(url, cache_dir),
        }
