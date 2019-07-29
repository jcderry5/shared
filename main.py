mport webapp2
import jinja2
import os


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        print("KMA")

class QuizPage(webapp2.RequestHandler):
    def get(self):
        print("Testing Text")

class LearnPage(webapp2.RequestHandler):
    def get(self):
        print("Testing Text")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Quiz',QuizPage),
    ('/Learn', LearnPage)
], debug=True)
