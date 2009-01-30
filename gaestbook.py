import cgi
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import *
from helpers import TemplateHelper

from facebook import Facebook
import settings

class MainPage(webapp.RequestHandler):
  def get(self):
    #TemplateHelper(self.response.out, 'index').render()
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)
    
    authors = {}

    TemplateHelper(self.response.out, 'gaestbook', {
      'user': None,
      'greetings': greetings,
      'authors': authors
    }).render()
  
  def post(self):
    # Initialize the Facebook Object.
    logging.debug('Before creating facebook instance')
    fb = Facebook(settings.key.api, settings.key.secret)
    logging.debug('Created Facebook instance')
    
    # Checks to make s  ure that the user is logged into Facebook.
    if fb.check_session(self.request):
      pass
    else:
      # If not redirect them to your application add page.
      url = fb.get_add_url()
      self.response.out.write('<fb:redirect url="' + url + '" />')
      return
  
    # Checks to make sure the user has added your application.
    if fb.added:
      pass
    else:
      # If not redirect them to your application add page.
      url = fb.get_add_url()
      self.response.out.write('<fb:redirect url="' + url + '" />')
      return

    # Get the information about the user.
    user = fb.users.getInfo(
      [fb.uid],
      ['uid', 'name', 'pic_small'])[0]
    logging.debug('Got user info')

    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)
    
    for greeting in greetings:
      greeting.fbinit(fb)

    TemplateHelper(self.response.out, 'gaestbook', {
      'user': Author(fb.uid, fb),
      'greetings': greetings
    }).render()

class Guestbook(webapp.RequestHandler):
  def post(self):
    fb = Facebook(settings.key.api, settings.key.secret)
    logging.debug('Created Facebook instance')

    # Checks to make s  ure that the user is logged into Facebook.
    if fb.check_session(self.request):
      pass
    else:
      # If not redirect them to your application add page.
      url = fb.get_add_url()
      self.response.out.write('<fb:redirect url="' + url + '" />')
      return

    # Checks to make sure the user has added your application.
    if fb.added:
      pass
    else:
      # If not redirect them to your application add page.
      url = fb.get_add_url()
      self.response.out.write('<fb:redirect url="' + url + '" />')
      return
    
    greeting = Greeting()
    greeting.uid = fb.uid
    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')

class TestPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("hej")
    logging.debug("testpage")

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  logging.debug("starting app...")
  run_wsgi_app(application)

if __name__ == "__main__":
  main()