from google.appengine.ext import ndb

class User(ndb.Model):
  username = ndb.StringProperty()
  password = ndb.StringProperty()
  email= ndb.StringProperty()
  learning_style = ndb.StringProperty()
