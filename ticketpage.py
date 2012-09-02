'''
Created on Aug 29, 2012

@author: jchen
'''
import urllib
import types
import webapp2
from google.appengine.api import urlfetch
from google.appengine.ext import db
from match import *

class Ticket(db.Model):
    """Models client's email"""
    url = db.LinkProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty()
def ticket_url_key(url=None):
    return db.Key.from_path('ticket', url or 'default_url')

def isTicketAvailable(url=None):
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        final_url = result.final_url
        if final_url == None:
            return 1
        if final_url.find("error") != -1:
            return 0
        
    else:
        return -1
class ShowTickets(webapp2.RequestHandler):
    def get(self):
        q = Match.all() 
        results = q.fetch(10000)
        self.response.out.write("<html><body>")
        for r in results:
            self.response.out.write("<div>")
            url = r.url
#            ticket_status = isTicketAvailable(url)
    #        self.response.out.write("%s<br/>"%ticket_status)
#            writeTicketAvailable(url, ticket_status)
            ticket_status = getTicketStatus(url)
            status_text = "unknown"
            if ticket_status != None:
    #            self.response.out.write("<b>%s</b> at %s, url: %s<br/>"%(ticket_status.status,ticket_status.date,ticket_status.url))
                if ticket_status.status == "1":
                    status_text = "available"
                elif ticket_status.status == "0":
                    status_text = "not available"
                self.response.out.write("<b>%s</b> at %s, url: %s" % (status_text, ticket_status.date, ticket_status.url))
                self.response.out.write("</body></html>")
            else:
                self.response.out.write("<b>No record</b>, url: %s" % (url))

            self.response.out.write("</div>")
        self.response.out.write("</body></html>")

def writeTicketAvailable(url, t_status):
    ticket = Ticket(parent=ticket_url_key(url))
    ticket.url = url
#    print t_status
    ticket.status = str(t_status)
    ticket.put()
def getTicketStatus(url):
    q = Ticket.all() 
    q.ancestor(ticket_url_key(url))
    q.filter('url = ', url)
    q.order("-date")
    results = q.fetch(1)
    for r in results:
        return r
def getTicketStatusChange(url):
    q = Ticket.all() 
    q.ancestor(ticket_url_key(url))
    q.filter('url = ', url)
    q.order("-date")
    results = q.fetch(2)
    status_change=False
    
    status=None
    available=False
    for r in results:
        if status==None:
            status=r.status
            if status=="1":
                available=True
        else:
            if status!=r.status:
                status_change=True
    return (status_change,available)
