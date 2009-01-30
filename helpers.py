import os

from google.appengine.ext.webapp import template

class TemplateHelper():
  def __init__(self, writer, template = "", values = {}):
    self.writer = writer
    
    if template:
      self.path = os.path.join(os.path.dirname(__file__),
        'templates/%s.html' % template)
    else:
      self.path = None

    self.values = values

  def render(self):
    self.writer.write(template.render(self.path, self.values))
