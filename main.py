mport webapp2
import jinja2
import os


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomePage(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/home.html')

        print("KMA")

class QuizPage(webapp2.RequestHandler):
    def get(self):
        quiz_template = jinja_env.get_template('templates/quiz.html')

class VisualPage(webapp2.RequestHandler):
    def get(self):
        visual_template = jinja_env.get_template('templates/visual.html')

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('templates/profile.html')


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/Quiz',QuizPage),
    ('/Visual', VisualPage),
    ('Profile', ProfilePage)
], debug=True)
