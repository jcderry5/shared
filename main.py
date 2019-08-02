import webapp2
import jinja2
import os
import json
import base64
import time

from google.appengine.api import images
from google.appengine.api import users, urlfetch
from model import H2JUser
from seed_user_db import seed_data



jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Image(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            h2j_user = H2JUser.query().filter(H2JUser.email == email_address).get()
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(h2j_user.profile_pic)
        else:
            self.response.out.write('No image')

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

             h2j_ls = " "

             if h2j_user:
                 h2j_ls = h2j_user.learning_style

             home_dict = {
                "h2j_user" : h2j_user,
                "learning_style" : h2j_ls
             }
             self.response.write(home_template.render(home_dict))
        else:
            print("No user exists")
            # This line creates a URL to log in with your Google Credentials.
            login_url = users.create_login_url('/')

            # This line uses string templating to create an anchor (link) element.
            login_html_element = '<a href="%s">Sign in</a>' % login_url
            # This line puts that URL on screen in a clickable anchor elememt.
            login_dict = {
                "login_url" : login_url
            }
            self.response.write(home_template.render(login_dict))


    def post(self):

        if self.request.get("first_name") and self.request.get("last_name"):
            # This will run if we have fill in the form but haven't put into db
            temp_first_name = self.request.get("first_name")
            temp_last_name = self.request.get("last_name")

            if self.request.get("pic"):
                profile_pic = self.request.get("pic")
                pic_resize = images.resize(profile_pic, 256, 256)
            else:
                pic_resize = None


            user = users.get_current_user()
            temp_email_address = user.nickname()
            H2JUser(email=temp_email_address,
                    first_name=temp_first_name, last_name=temp_last_name, profile_pic=pic_resize).put()

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
        user = users.get_current_user()
        email_address = user.nickname()
        h2j_user = H2JUser.query().filter(H2JUser.email == user.nickname()).get()

        v_learn = 0
        a_learn = 0
        r_learn = 0

        all_ques = []
        all_ques.append(self.request.get("q-1"))
        all_ques.append(self.request.get("q-2"))
        all_ques.append(self.request.get("q-3"))
        all_ques.append(self.request.get("q-4"))
        all_ques.append(self.request.get("q-5"))

        for value in all_ques:
            if value == "v":
                v_learn += 1
            elif value == "a":
                a_learn += 1
            elif value == "r":
                r_learn += 1
        if v_learn == a_learn and v_learn > r_learn:
            h2j_user.learning_style = "Visual"
            h2j_user.put()
            return webapp2.redirect("/Visual")

        elif a_learn == r_learn and a_learn > v_learn:
            h2j_user.learning_style = "Auditory"
            h2j_user.put()
            return webapp2.redirect("/Auditory")

        elif r_learn == v_learn and r_learn > a_learn:
            h2j_user.learning_style = "Reading/Writing"
            h2j_user.put()
            return webapp2.redirect("/Writing")


        elif v_learn > a_learn and v_learn >r_learn:
            #use is a visual learner
            h2j_user.learning_style = "Visual"
            h2j_user.put()
            # self.response.write(jinja_env.get_template('templates/visual.html').render())
            return webapp2.redirect("/Visual")
        elif a_learn > v_learn and a_learn > r_learn:
            #use is a aural learner
            h2j_user.learning_style = "Auditory"
            h2j_user.put()
            return webapp2.redirect("/Auditory")
        elif r_learn > v_learn and r_learn > a_learn:
            #use is a reading/writing learner
            h2j_user.learning_style = "Reading/Writing"
            h2j_user.put()
            return webapp2.redirect("/Writing")

    def get(self):
        quiz_template = jinja_env.get_template('templates/quiz.html')


        self.response.write(quiz_template.render())

class VisualPage(webapp2.RequestHandler):
    def get(self):
        visual_template = jinja_env.get_template('templates/visual.html')

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

             h2j_ls = ""

             if h2j_user:
               h2j_ls = h2j_user.learning_style

               visual_dict = {
               "h2j_user" : h2j_user,
               "learning_style" : h2j_ls
               }

               self.response.write(visual_template.render(visual_dict))
             else:
                 self.response.write(visual_template.render())

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_env.get_template('templates/profile.html')

        user = users.get_current_user()
        if user:
             # Create the sign out link (for later use).
             signout_url = users.create_logout_url('/')
             # If the user is logged in, get their email address.
             email_address = user.nickname()
             # Then query Datastore to see if a user with this email has registered as
             # a H2JUser before.
             h2j_user = H2JUser.query().filter(H2JUser.email == email_address).get()
             # If the query is successful, the variable will have a user in it, so the

             h2j_ls = " "
             var_picture = " "

             if h2j_user:
                 h2j_ls = h2j_user.learning_style
                 h2j_fn = h2j_user.first_name
                 h2j_ln = h2j_user.last_name
                 if h2j_user.profile_pic:
                     var_picture = 'data:image/png;base64,' + base64.b64encode(h2j_user.profile_pic)
                 else:
                     var_picture = "https://i.stack.imgur.com/34AD2.jpg"


             profile_dict = {
                "h2j_user" : h2j_user,
                "learning_style" : h2j_ls,
                "first_name" : h2j_fn,
                "last_name" : h2j_ln,
                "email" : email_address,
                "sign_out_link" : signout_url,
                "picture" : var_picture
             }
             self.response.write(profile_template.render(profile_dict))
        else:
            self.response.write(profile_template.render())

class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_data()

class AuditoryPage(webapp2.RequestHandler):
    def get(self):
        aural_template = jinja_env.get_template('templates/aural.html')

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

             h2j_ls = ""

             if h2j_user:
               h2j_ls = h2j_user.learning_style

               aural_dict = {
               "h2j_user" : h2j_user,
               "learning_style" : h2j_ls
               }

               self.response.write(aural_template.render(aural_dict))
             else:
                 self.response.write(aural_template.render())

class WritingPage(webapp2.RequestHandler):
    def get(self):
        writing_template = jinja_env.get_template('templates/writing.html')

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

             h2j_ls = ""

             if h2j_user:
                 h2j_ls = h2j_user.learning_style

                 writing_dict = {
                 "h2j_user" : h2j_user,
                 "learning_style" : h2j_ls
                 }
                 time.sleep(0.1)
                 self.response.write(writing_template.render(writing_dict))
             else:
                 time.sleep(0.1)
                 self.response.write(writing_template.render())

class AboutPage(webapp2.RequestHandler):
    def get(self):
        about_template = jinja_env.get_template('templates/about.html')


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

             h2j_ls = ""

             if h2j_user:
               h2j_ls = h2j_user.learning_style

               about_dict = {
               "h2j_user" : h2j_user,
               "learning_style" : h2j_ls
               }

               self.response.write(about_template.render(about_dict))
             else:
                 self.response.write(writing_template.render())

class StatisticsPage(webapp2.RequestHandler):
    def get(self):
        stats_template = jinja_env.get_template('templates/stats.html')

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

             h2j_ls = ""

             if h2j_user:
                h2j_ls = h2j_user.learning_style

                stats_dict = {
                "h2j_user" : h2j_user,
                "learning_style" : h2j_ls
                }

                self.response.write(stats_template.render(stats_dict))
             else:
                self.response.write(about_template.render())

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/Quiz',QuizPage),
    ('/ProfileImage', Image),
    ('/Visual', VisualPage),
    ('/Profile', ProfilePage),
    ('/seed-data', LoadDataHandler),
    ('/Auditory', AuditoryPage),
    ('/Writing', WritingPage),
    ('/About', AboutPage),
    ('/Statistics', StatisticsPage)

], debug=True)
