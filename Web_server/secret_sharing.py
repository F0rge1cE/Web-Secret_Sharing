#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail, app_identity

import httplib2
import os
import oauth2client
from oauth2client import file 
# from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import apiclient
import googleapiclient
from googleapiclient import discovery
#from apiclient import discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

import jinja2
import webapp2

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


class File(ndb.Model):

    filt_name = ndb.StringProperty(indexed=False)
    N_share = ndb.StringProperty(indexed=False)
    K_require = ndb.StringProperty(indexed=False)
    hash_value = ndb.StringProperty(indexed=False)





# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('./template/main.html')
        self.response.write(template.render(template_values))
# [END main_page]

class Encrypt(webapp2.RequestHandler):
    def get(self):
        except_ = self.request.get('except', False)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'except' : except_
        }

        template = JINJA_ENVIRONMENT.get_template('./template/encrypt.html')
        self.response.write(template.render(template_values))

    def post(self):
        try:
            #file = self.request.POST.get('raw_file').file.read()

            uploaded_file = self.request.POST.get('raw_file')   # uploaded_file is an file object
            content = uploaded_file.file.read()
            file_name = uploaded_file.filename



        except:
            query_params = {
                'except' : True
            }
            self.redirect('/encrypt?' + urllib.urlencode(query_params))
        else:
            name = self.request.get('name')
            N_share = self.request.get('N_share')
            K_require = self.request.get('K_require')
            print("****************************************")
            print(content)
            print("add encrypt algorithm here")
            print("****************************************")

            query_params = {
                'num' : N_share
            }
            self.redirect('/email?' + urllib.urlencode(query_params))


# [START guestbook]

# [END guestbook]
class Decrypt(webapp2.RequestHandler):

    def get(self):
        except_ = self.request.get('except', False)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'except' : except_
        }

        template = JINJA_ENVIRONMENT.get_template('./template/decrypt.html')
        self.response.write(template.render(template_values))

    def post(self):
        try:



            file = self.request.POST.getall('raw_file')
            name = self.request.get('name')
            for f in file:
                sub_file = f.file.read()
                print("****************")
                print(sub_file)
            # add reconstruct algorithm here
        except:
            query_params = {
                'except' : True
            }
            self.redirect('/decrypt?' + urllib.urlencode(query_params))
        else:
            
            query_params = {
                'decrypt': True,
            }
            self.redirect('/success?' + urllib.urlencode(query_params))

class Success(webapp2.RequestHandler):

    def get(self):
        encrypt = self.request.get('encrypt', False)
        decrypt = self.request.get('decrypt', False)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'decrypt' : decrypt,
            'encrypt' : encrypt
        }

        template = JINJA_ENVIRONMENT.get_template('./template/success.html')
        self.response.write(template.render(template_values))

class Email(webapp2.RequestHandler):

    def get(self):
        num = int(self.request.get('num'))
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        lis = []
        for i in range(num):
            lis.append(i + 1)
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'lis' : lis
        }

        template = JINJA_ENVIRONMENT.get_template('./template/email.html')
        self.response.write(template.render(template_values))

    def post(self):
        email = self.request.POST.getall('email')
        print("*********************************")
        for i in email:
            print(i)
        print("*********************************")
        for i in email:
            mail.send_mail(sender='{}@ece6102assignment4.gserviceaccount.com'.format(
            app_identity.get_application_id()),
                       to=i,
                       subject="Decrypted shareds",
                       body="""
                            Attached is the document file you requested.
                            The example.com Team
                            """,
                       attachments=[("test.share", "heiheihei")])



        query_params = {
            'encrypt': True,
        }
        self.redirect('/success?' + urllib.urlencode(query_params))


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/encrypt', Encrypt),
    ('/decrypt', Decrypt),
    ('/success', Success),
    ('/email', Email)
], debug=True)
# [END app]
