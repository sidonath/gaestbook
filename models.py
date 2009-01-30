import logging
from google.appengine.ext import db

class Greeting(db.Model):
  uid = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  
  _facebook = None
  _author = None
  
  def fbinit(self, facebook):
    self._facebook = facebook
    self._author = None
    logging.debug("Greeting: Facebook initialized")
    
  def author(self):
    if self._author:
      logging.debug("Greeting: Author returned")
      return self._author
    elif self._facebook:
      logging.debug("Greeting: Author will be loaded")
      self._author = Author(self.uid, self._facebook)
      return self._author
    else:
      logging.debug("Greeting: Neither facebook nor author were init'd")
      return None

class Author(object):
  def __init__(self, uid="", facebook=None):
    self.uid = uid

    if facebook:
      self.load(facebook)
    elif uid == "":
      self.name = "Test User"
      self.pic_small = ''
      self.pic_square = ''
      
  
  def load(self, facebook):
    data = facebook.users.getInfo(
      [self.uid],
      ['uid', 'name', 'pic_small', 'pic_square'])[0]
    self.name = data['name']
    self.pic_small = data['pic_small']
    self.pic_square = data['pic_square']