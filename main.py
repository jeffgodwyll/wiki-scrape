import tornado.web
import tornado.wsgi

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


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(TEMPLATE)

    def post(self):
        pass


app = tornado.web.Application([
    (r"/", MainHandler)],
)
app = tornado.wsgi.WSGIAdapter(app)
