from google.appengine.ext import db

class LastLight(db.Model):
  value = db.IntegerProperty(required=True)
  updated = db.DateTimeProperty(auto_now=True)
