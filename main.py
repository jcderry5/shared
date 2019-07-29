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
          # Create the sign out link (for later use).
          signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
          # If the user is logged in, get their email address.
          email_address = user.nickname()
          # Then query Datastore to see if a user with this email has registered as
          # a CssiUser before.
          cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
          # If the query is successful, the variable will have a user in it, so the
          # following code will run.
          if cssi_user:
            self.response.write(
              "Looks like you're registered. Thanks for using our site!")
          # if the query wasn't successful, the variable will be empty, so this code
          # will run instead.
          else:
            self.response.write(
              "Looks like you aren't a CSSI User. Please sign up.")
        else:
      # This line creates a URL to log in with your Google Credentials.
      login_url = users.create_login_url('/')
      # This line uses string templating to create an anchor (link) element.
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      # This line puts that URL on screen in a clickable anchor elememt.
      self.response.write('Please log in.<b>' + login_html_element)

class AuditoryPage(webapp2.RequestHandler):
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
    ('/Auditory', AuralPage),
    ('/Writing', WritingPage)
], debug=True)
