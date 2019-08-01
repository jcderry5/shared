from google.appengine.ext import ndb

class H2JUser(ndb.Model):
  learning_style = ndb.StringProperty()
  email = ndb.StringProperty()
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  profile_pic = ndb.BlobProperty()
