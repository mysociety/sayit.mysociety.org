import os

import bs4

import utils
import requests
import requests_cache
requests_cache.install_cache(os.path.join(utils.CACHE_DIR, 'labour'))


def get_url(url):
    resp = requests.get(url)
    return bs4.BeautifulSoup(resp.text)


def get_speeches(index_url):
    while index_url:
        print 'Accessing {}'.format(index_url)
        index_soup = get_url(index_url)
        articles = index_soup.findAll('div', {'class': 'article'})

        for article in articles:
            title_element = article.find('h3', {'class': 'article-title'})
            title = title_element.text
            article_url = title_element.a['href']

            speech_soup = get_url(article_url)

            yield {
                'title': title,
                'url': article_url,
                'soup': speech_soup,
                }

        next_text = index_soup.find(text=u'next \xbb')

        if next_text:
            index_url = next_text.parent['href']
        else:
            print "BREAKING - No 'next' link found."
            index_url = None
