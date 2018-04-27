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

import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import apiclient
#from apiclient import errors, discovery
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

# def get_credentials():
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'gmail-python-email-send.json')
#     store = oauth2client.file.Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         credentials = tools.run_flow(flow, store)
#         print('Storing credentials to ' + credential_path)
#     return credentials

# def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = apiclient.discovery.build('gmail', 'v1', http=http)
#     if attachmentFile:
#         message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
#     else: 
#         message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
#     result = SendMessageInternal(service, "me", message1)
#     return result

# def SendMessageInternal(service, user_id, message):
#     try:
#         message = (service.users().messages().send(userId=user_id, body=message).execute())
#         print('Message Id: %s' % message['id'])
#         return message
#     except apiclient.errors.HttpError as error:
#         print('An error occurred: %s' % error)
#         return "Error"
#     return "OK"

# def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = to
#     msg.attach(MIMEText(msgPlain, 'plain'))
#     msg.attach(MIMEText(msgHtml, 'html'))
#     return {'raw': base64.urlsafe_b64encode(msg.as_string())}





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
            file = self.request.POST.get('raw_file').file.read()
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
            print(file)
            print("add encrypt algorithm here")
            print("****************************************")


            #add gmail api here
            to = "xuxy1994@gmail.com"
            sender = "guoyuanwu666@gmail.com"
            subject = "subject"
            msgHtml = file
            msgPlain = "Hi\nPlain Email"
            #SendMessage(sender, to, subject, msgHtml, msgPlain)



            query_params = {
                'encrypt': True,
            }
            self.redirect('/success?' + urllib.urlencode(query_params))


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


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/encrypt', Encrypt),
    ('/decrypt', Decrypt),
    ('/success', Success)
], debug=True)
# [END app]
