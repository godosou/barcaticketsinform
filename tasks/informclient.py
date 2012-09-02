'''
Created on Aug 29, 2012

@author: jchen
'''
from google.appengine.api import mail
import web2
def sendmailfunc(available, ticketurl, email):
    avail_text=""
    if available==1:
        avail_text =" available"
    else:
        avail_text =" unavailable"
    title="You have ticket becomes %s"%avail_text
    body="You have ticket becomes %s, please visit following url to buy it %s "%(avail_text,ticketurl)
    message=mail.EmailMessage(subject=title)
    message.sender = "godosou@gmail.com"
    message.to=email
    message.body=body
    message.send()
class sendmail(webapp2.RequestHandler):
    def post(self):
        available= int(self.request.get('available'))
        ticketurl=self.request.get('ticketurl')
        email=self.request.get('email')
        self.reponse.out("%s"%available,email)
        sendmailfunc(available,ticketurl)
    def get(self):
        self.response.out.write("out")
        pass