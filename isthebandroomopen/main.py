#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from models import LastLight
from datetime import datetime
from datetime import timedelta
import jinja2
import os

LIGHT_THRESH = 400
DISCONNECT_THRESH = 5*60 # seconds

jinja_environment = jinja2.Environment (
  loader=jinja2.FileSystemLoader ((os.path.dirname (__file__), 'templates')), extensions=[])

class HelpHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("disconnected.html")
        self.response.out.write(template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        lastLight = LastLight.all().get()
        if not lastLight:
            lastLight = LastLight(value=0)
            lastLight.put()
        
        nw = datetime.now()
        template = None
        if (lastLight.updated < (nw - timedelta(seconds=DISCONNECT_THRESH))):
            template = jinja_environment.get_template("disconnected.html")
        elif (lastLight.value > LIGHT_THRESH):
            template = jinja_environment.get_template("yespipes.html")
        else:
            template = jinja_environment.get_template("nopipes.html")
        self.response.out.write(template.render())

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        lastLight = LastLight.all().get()
        if not lastLight:
            lastLight = LastLight(value=0)
            
        v = self.request.get('v')
        
        try:
            lastLight.value = int(v)
            lastLight.put()
            self.response.out.write('OK')
        except:
            self.response.out.write('BAD')
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/help', HelpHandler),
	('/update', UpdateHandler),
], debug=True)
