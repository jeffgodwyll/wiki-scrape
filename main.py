import logging
from collections import defaultdict

import json

import tornado.web

import tornado.wsgi

import requests
import requests_toolbelt.adapters.appengine

from google.appengine.ext import ndb
# from webapp2_extras.appengine.auth.models import Unique

# make requests use urlfetch
requests_toolbelt.adapters.appengine.monkeypatch()


BASE_URL = 'https://en.wikipedia.org/wiki%s'

TEMPLATE = """
<html>
<body>
  <form action="/" method="post">
    <div>
      <input name='article'></input>
    </div>
    <div>
      <input type="submit" value="submit"></input>
    </div>
  </form>
</body>
</html>
"""

# logger
logger = logging.getLogger(__name__)


class Article(ndb.Model):
    '''Datastore Article entity model
    '''
    url = ndb.StringProperty()
    # title = ndb.StringProperty(required=False)
    scraped = ndb.JsonProperty()

    # TODO: Check for existing article and increase count
    # use https://github.com/jeffgodwyll/qod-api/blob/master/main.py#L50 as base


def tree():
    ''' Returns tree data structure of a dict with trees as default values
    '''
    return defaultdict(tree)


def is_url():
    '''Returns True if url is valid
    '''
    # TODO: validate url
    pass


def get_article(url):
    '''Return wikipedia article text
    '''
    # TODO: validate url
    try:
        article = requests.get(url)
        return article.text
    except requests.exceptions.RequestException as e:
        logger.error(e)


def get_links(article):
    '''Return all links in wikipedia article

    Idea from http://stackoverflow.com/a/1081404
    '''
    links = []
    start_tag = '<a href="/wiki'
    end_tag = '">'
    for text in article.split('</a>'):
        if '<a href' in text:
            try:
                ind = text.index(start_tag)
                text = text[ind+len(start_tag):]
                end = text.index(end_tag)
            except:
                pass
            else:
                link = text[:end]
                # articles have titles, class=mw-redirect are not articles too
                if 'title=' in link and 'class' not in link:
                    a = tuple(link.split('" title="'))
                    # logger.info(a)
                    # logger.info('url: {}, title: {}'.format(url, title))
                    links.append(a)
    return links


class MainHandler(tornado.web.RequestHandler):
    '''Homepage request handler
    '''

    # TODO: create recursive function
    def follow(self, url, depth=3):
        '''Recursively follow links'''
        pass

    def get(self):
        self.write(TEMPLATE)
        self.write('<br>')
        self.write('<br>')
        self.write('<hr>')
        articles = Article.query().fetch()
        self.write(str(articles))

    def post(self):
        '''Handle post request
        '''
        l = 6
        url = self.get_argument('article')
        article_text = get_article(url)
        links = get_links(article_text)

        scraped = tree()

        # TODO: refactor into recursive function
        # first 6 links
        for i, l1 in enumerate(links[:l]):

            '''self.write('<br>')
            self.write('<br>')
            self.write('* ' + l1[0])
            self.write('<br>')'''

            # check if url has been scraped already and increase count in model
            # entity use ff transaction as base:
            # https://github.com/jeffgodwyll/qod-api/blob/master/main.py#L50
            l1_url = BASE_URL % l1[0]
            link_text = get_article(l1_url)
            child_links = get_links(link_text)
            for i2, l2 in enumerate(child_links[:l]):
                l2_url = BASE_URL % l2[0]
                link_text = get_article(l2_url)
                child_links2 = get_links(link_text)

                for i3, l3 in enumerate(child_links2[:l]):

                    scraped['root'][url][i]['url'][l1[0]][i2]['url'][l2[0]][i3]['url'] = l3[0]
                    scraped['root'][url][i]['url'][l1[0]][i2]['url'][l2[0]][i3]['title'] = l3[1]
                    scraped['root'][url][i]['url'][l1[0]][i2]['title'] = l2[1]
                    scraped['root'][url][i]['title'] = l1[1]

        self.write('<pre>{}</pre>'.format(
            json.dumps(scraped, sort_keys=True, indent=2)))
        article = Article(
            url=url,
            scraped=json.loads(json.dumps(scraped))
        )
        article.put()


app = tornado.web.Application([
    (r"/", MainHandler)],
)
app = tornado.wsgi.WSGIAdapter(app)
