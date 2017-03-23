from datetime import datetime
import re
import string

from speeches.utils.scraping import ParserSection as Section, ParserSpeech as Speech

from brexit.names import fix_name

def parse_transcript(text, url, para_min_indent=None):
    print "PARSING %s" % url

    page, num = 1, 1

    indent = ' ' * 3
    speech = None
    Speech.reset(True)

    for line in text:
        # Page break
        if '\014' in line:
            page += 1
            num = 1
            continue

        # Empty line
        if re.match('\s*$', line):
            continue

        # Just after last line, there should be a page number
        if num == 26:
            m = re.match(' +(\d+)$', line)
            assert int(m.group(1)) == page
            continue

        # Let's check we haven't lost a line anywhere...
        assert re.match(' *%d( |$)' % num, line), '%s != %s' % (num, line)

        line = re.sub('^ *%d(%s|$)' % (num, indent), '', line)

        # Okay, here we have a non-empty, non-page number, non-index line of just text
        # if para_min_indent:
        #     print page, num, '!', line.encode('utf-8')

        num += 1

        # Empty line
        if re.match('\s*$', line):
            continue

        if re.match(' *DRAFT TRANSCRIPT$', line):
            continue

        if re.match(' *INDEX$', line):
            break

        # Date at start
        m = re.match(' *((Mon|Tues|Wednes|Thurs|Fri)day,? ?)?\d+ (September|October|November|December|January|February|March|April|May|June|July) 201\d+$', line)
        if m:
            continue

        m = re.match(' *(\(.*\))(?:break|s)?$', line)
        if m:
            try:
                line = m.group(1)
                line = line.replace('O2', '02')
                if re.match('\(1[3-9]\.', line):
                    time_format = '(%H.%M %p)'
                else:
                    time_format = '(%I.%M %p)'
                Speech.current_time = datetime.strptime(line, time_format).time()
            except:
                if para_min_indent:
                    #print speech.text
                    yield speech
                if 'The luncheon adjournment' in line and not Speech.current_time:
                    continue
                speech = Speech( speaker=None, text=line )
            continue

        # Headings
        m = re.match('Opening statement by [A-Z ]*$|Submissions? (in reply )?by [A-Z ]*(?: \(continued\))?$', line.strip())
        if m:
            Speech.current_section = Section( heading=string.capwords(line.strip()) )
            continue

        # New speaker
        m = re.match(' *((?:[A-Z -]|Mc)+): (.*)', line)
        if m:
            if para_min_indent:
                #print speech.text if speech else None
                yield speech
            speaker = fix_name(m.group(1))
            speech = Speech( speaker=speaker, text=m.group(2) )
            continue

        if not para_min_indent:
            yield page, num-1, line
            continue

        # New paragraph if indent at least 8 spaces
        m = re.match(' ' * para_min_indent[page], line)
        if m:
            speech.add_para(line.strip())
            continue

        # If we've got this far, hopefully just a normal line of speech
        speech.add_text(line.strip())

    if para_min_indent:
        #print speech.text
        yield speech
