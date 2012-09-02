'''
Created on Aug 29, 2012

@author: jchen
'''
from google.appengine.api import taskqueue
def checkMatchTickets():
    q=taskqueue.Queue('checkticket')
    q.add(url='/checkticket')

if __name__=="__main__":
    checkMatchTickets()