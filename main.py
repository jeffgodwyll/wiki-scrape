import logging

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
    title = ndb.StringProperty(required=False)

    # TODO: Check for existing article and increase count
    # use https://github.com/jeffgodwyll/qod-api/blob/master/main.py#L50 as base


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

    # TODO: look at this attempt at  a recursive function later
    # def follow(self, url, depth=3):
    #     article_text = get_article(url)
    #     links = get_links(article_text)
    #     # follow first 6 links
    #     while depth > 0:
    #         for link in links[:6]:
    #             self.write('<br>')
    #             self.write(link[0])
    #             self.write('<br>')
    #             logger.info(link[0])
    #             link_url = BASE_URL % link[0]
    #             self.follow(link_url, depth)
    #         depth -= 1
    #         # self.follow(link_url, depth)

    def get(self):
        self.write(TEMPLATE)

    # TODO: Specify datastore root entity
    # root = Article()
    # root.url = url
    # root_key = root.put()

    def post(self):
        '''Handle post request
        '''
        url = self.get_argument('article')
        article_text = get_article(url)
        links = get_links(article_text)
        # TODO: refactor into recursive function
        # first 6 links

        # level_1 = []
        # level_2 = []
        for link in links[:6]:

            self.write('<br>')
            self.write('<br>')
            self.write('* ' + link[0])
            self.write('<br>')

            # TODO: add parent
            # check if url has been scraped already and increase count in model
            # entity use ff transaction as base:
            # https://github.com/jeffgodwyll/qod-api/blob/master/main.py#L50
            article = Article(url=url, title=link[1])
            article.put()
            link_url = BASE_URL % link[0]
            link_text = get_article(link_url)
            child_links = get_links(link_text)
            for link in child_links[:6]:
                article = Article(url=link_url, title=link[1])  # TODO: parent
                article.put()
                self.write('<br>')
                self.write('<br>')
                self.write('** ' + link[0])
                # level_2.append(link1[0])
                self.write('<br>')
                link_url = BASE_URL % link[0]
                link_text = get_article(link_url)
                child_links2 = get_links(link_text)
                for link in child_links2[:6]:
                    article = Article(url=link_url, title=link[1])
                    article.put()
                    self.write('<br>')
                    self.write('*** ' + link[0])


app = tornado.web.Application([
    (r"/", MainHandler)],
)
app = tornado.wsgi.WSGIAdapter(app)
