import logging

import tornado.web

import tornado.wsgi

import requests
import requests_toolbelt.adapters.appengine

# make requests use urlfetch
requests_toolbelt.adapters.appengine.monkeypatch()

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


def is_url():
    # TODO: validate url
    pass


def get_article(url):
    # TODO: validate url
    try:
        article = requests.get(url)
        return article.text
    except requests.exceptions.RequestException as e:
        logger.error(e)


def get_links(article):
    ''' Get all links in wikipedia article
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
                    logger.info(a)
                    # logger.info('url: {}, title: {}'.format(url, title))
                    links.append(a)
    return links


def follow(link):
    pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(TEMPLATE)

    def post(self):
        url = self.get_argument('article')
        article_text = get_article(url)
        links = get_links(article_text)
        # first 6 links
        for link in links[:6]:
            self.write(link[0])


app = tornado.web.Application([
    (r"/", MainHandler)],
)
app = tornado.wsgi.WSGIAdapter(app)
