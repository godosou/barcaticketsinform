'''
Created on Aug 29, 2012

@author: jchen
'''
import webapp2
from ticketchecker import *
from informclient import *
app = webapp2.WSGIApplication([('/checkticket',checkMatchTickets),
                               ('/sendmail',sendmail)],debug=True)