import webapp2
import jinja2
import os
import json

from google.appengine.api import users
from model import User
from seed_user_db import seed_data



jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomePage(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_env.get_template('templates/home.html')

        user = users.get_current_user()
        if user:
          # The if block only runs if the user IS logged in.
          # The user has a method called `nickname()` that looks up their email.
          # We can use this information to show the user who they're logged in as.
          email_address = user.nickname()
          # Generate a sign out link - this does it all in one line.
          logout_link_html = '<a href="%s">sign out</a>' % (
                                users.create_logout_url('/'))
          # Show that sign out link on screen:
          self.response.write(
                "You're logged in as " + email_address + "<br>" + logout_link_html)
        else:
          # This line creates a URL to log in with your Google Credentials.
          login_url = users.create_login_url('/')
          # This line uses string templating to create an anchor (link) element.
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          # This line puts that URL on screen in a clickable anchor elememt.
          self.response.write('Please log in.<b>' + login_html_element)

class AuralPage(webapp2.RequestHandler):
    def get(self):
        quiz_template = jinja_env.get_template('templates/aural.html')

class WritingPage(webapp2.RequestHandler):
    def get(self):
        quiz_template = jinja_env.get_template('templates/writing.html')


class QuizPage(webapp2.RequestHandler):
    def get(self):
        quiz_template = jinja_env.get_template('templates/quiz.html')

class VisualPage(webapp2.RequestHandler):
    def get(self):
        visual_template = jinja_env.get_template('templates/visual.html')

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('templates/profile.html')

class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_data()



app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/Quiz',QuizPage),
    ('/Visual', VisualPage),
    ('/Profile', ProfilePage),
    ('/seed-data', LoadDataHandler),
], debug=True)
