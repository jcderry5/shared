import webapp2
import jinja2
import os
import json

from google.appengine.api import users, urlfetch
from model import H2JUser
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
          # a H2JUser before.
          h2j_user = H2JUser.query().filter(H2JUser.email == email_address).get()
          # If the query is successful, the variable will have a user in it, so the
          # following code will run.

          home_dict = {
              "h2j_user" : h2j_user
          }
          self.response.write(home_template.render(home_dict))


    def post(self):
        if self.request.get("first_name") and self.request.get("last_name"):
            # This will run if we have fill in the form but haven't put into db
            temp_username = self.request.get("username")
            temp_password= self.request.get("password")
            temp_first_name = self.request.get("first_name")
            temp_last_name = self.request.get("last_name")
            user = users.get_current_user()
            temp_email_address = user.nickname()
            H2JUser(username=temp_username, password=temp_password, email=temp_email_address,
                    first_name=temp_first_name, last_name=temp_last_name).put()
            return webapp2.redirect("/Quiz")


        else:
          # This line creates a URL to log in with your Google Credentials.
          login_url = users.create_login_url('/')
          # This line uses string templating to create an anchor (link) element.
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          # This line puts that URL on screen in a clickable anchor elememt.
          self.response.write('Please log in.<b>' + login_html_element)


class QuizPage(webapp2.RequestHandler):
    def post(self):
        quiz_template = jinja_env.get_template('templates/quiz.html')
        que_1 = self.request.get("q-1")
        que_2 = self.request.get("q-2")
        que_3 = self.request.get("q-3")
        que_4 = self.request.get("q-4")
        que_5 = self.request.get("q-5")

    def get(self):
        quiz_template = jinja_env.get_template('templates/quiz.html')
        self.response.write(quiz_template.render())


class VisualPage(webapp2.RequestHandler):
    def get(self):
        visual_template = jinja_env.get_template('templates/visual.html')

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('templates/profile.html')

class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_data()


class AuditoryPage(webapp2.RequestHandler):
    def get(self):
        khan= 'http://www.khanacademy.org/api/v1/topictree'
        result = urlfetch.fetch(khan).content

        quiz_template = jinja_env.get_template('templates/aural.html')

class WritingPage(webapp2.RequestHandler):
    def get(self):
        quiz_template = jinja_env.get_template('templates/writing.html')






app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/Quiz',QuizPage),
    ('/Visual', VisualPage),
    ('/Profile', ProfilePage),
    ('/seed-data', LoadDataHandler),
    ('/Auditory', AuditoryPage),
    ('/Writing', WritingPage)
], debug=True)
