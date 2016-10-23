import urlparse
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


def get_sheet_id(url):
    path = urlparse.urlsplit(url).path
    try:
        sheet_id = path.split('/')[3]
    except IndexError:
        logger.exception('url passed is {}'.format(url))
        sheet_id = ''
    return sheet_id


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
    links = []
    start_tag = '<a href="/wiki'
    end_tag = '">'
    for text in article.split("</a>"):
        if "<a href" in text:
            try:
                ind = text.index(start_tag)
                text = text[ind+len(start_tag):]
                end = text.index(end_tag)
            except:
                pass
            else:
                link = text[:end]
                a = link.split('title')
                logger.info(a)
                links.append(text[:end])
    return links


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(TEMPLATE)

    def post(self):
        url = self.get_argument('article')
        article_text = get_article(url)
        links = get_links(article_text)
        self.write(''.join(links))


app = tornado.web.Application([
    (r"/", MainHandler)],
)
app = tornado.wsgi.WSGIAdapter(app)
