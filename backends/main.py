'''
Created on Aug 29, 2012

@author: jchen
'''
import webapp2
app = webapp2.WSGIApplication([('/ticketchecker', checkMatchTickets)], debug=True)
