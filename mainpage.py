'''
Created on Aug 29, 2012

@author: jchen
'''
import webapp2
import cgi
import datetime
from google.appengine.ext import db
from ticketpage import *
from match import *
from google.appengine.api import taskqueue

from google.appengine.api import mail
def informClient(url, available):
    clients=Client.all()
    clients.filter('ticketurl = ',url)
    results = clients.fetch(10000)
    recepients=[]
    for r in results:
        recepients.append(r.email)
    sendmail(available,url,recepients)
#        q=taskqueue.Queue('sendmail')
#        taskqueue.add(url='/tasks/sendmail', params={'available': str(available), 'ticketurl':url,'email':r.email})
class changeTicketStatus(webapp2.RequestHandler):
    def get(self):
        url = "https://entrades.fcbarcelona.cat/Ticketing/gestionURL?bean=estadoCompra&accion=iniciarCompra&aforo=&idCompeticion=001&jornada=07&lang=en"
        status = getTicketStatus(url)
        self.response.out.write("%s%s"%(status.status,url))
        new_status=str(1-int(status.status))
        writeTicketAvailable(status.url,new_status)
        new_status= getTicketStatus(url)
        status_change=getTicketStatusChange(url)
        if status_change[0]==True:
            informClient(url, status_change[1])
  
class checkMatchTicketHandler(webapp2.RequestHandler):
    def get(self):
        q=Match.all() 
        results=q.fetch(10000)
        for r in results:
            writeTicketAvailable(r.url, isTicketAvailable(r.url))
            status_change=getTicketStatusChange(r.url)
            if status_change[0]==True:
                informClient(url, status_change[1])
class Client(db.Model):
    """Models client's email"""
    name = db.StringProperty()
    email = db.EmailProperty()
    adddate=db.DateTimeProperty(auto_now_add=True)
    ticketurl=db.LinkProperty()
def client_email_key(client_email=None):
    return db.Key.from_path('client',client_email or 'default_client')
class AddEmail(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email')
        name = self.request.get('name')
        url  = 'https://entrades.fcbarcelona.cat/Ticketing/gestionURL?bean=estadoCompra&accion=iniciarCompra&aforo=&idCompeticion=001&jornada=07&lang=en'
        existing_requests=db.GqlQuery("SELECT * FROM Client WHERE email= :1 AND ticketurl= :2",email,url)
        results = existing_requests.fetch(1)

        flag=True
        for req in results:
            flag=False
            self.response.out.write('<div>Request by <b>%s</b>(%s) to %s already added at %s</div>'\
                                    %(req.name,req.email,req.ticketurl,req.adddate))
        if flag:
            self.response.out.write('<html><body><div> Your email address is: ')
            client=Client(parent=client_email_key(email))
            client.name=name
            client.email=email
            client.ticketurl=url
            client.put()
            self.response.out.write(cgi.escape(self.request.get('email')))
        ticket_status=getTicketStatus(url)
        avail=False
        if ticket_status=="1":
            avail=True
        sendmail(avail,url,cgi.escape(self.request.get('email')))
        self.response.out.write('</div></body></html>')
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']='text/html'   
        url='https://entrades.fcbarcelona.cat/Ticketing/gestionURL?bean=estadoCompra&accion=iniciarCompra&aforo=&idCompeticion=001&jornada=07&lang=en' 
        status = getTicketStatus(url)
        
        available=""   
        if status.status=="1":
            available="available"
        elif status.status=="0":
            available="unavailable"
        else:
            available="unknown"
              
        self.response.out.write("""
          <html>
            <body>
            <h1>Welcome to Barca - Real Madrid ticket informer</h1><br/>
            <div>The ticket availability is updated every 1 minute.<br/>
            The current status is: <b>%s</b>.<br/>
            You will be informed whenever a ticket becomes available.<br/>
            You can manually check at <a href='%s'>The official ticket page<a>
            <br/>Please provide your email if you want to be informed in real time
            </div>
              <form action="/addemail" method="post">
                <div><lable>Name:</label><input name="name" type="text"></input></div>
                <div><lable>Email:</label><input name="email" type="text"></input></div>
                <div><input type="submit" value="Inform me"></div>
              </form>
            </body>
          </html>"""%(available, url))

        self.response.write(' \n')
def sendmail(available, ticketurl, recepients):
        ticket_info=""
        if bool(available)==True:
            avail_text =" available"
            ticket_info="please visit following url to buy it %s"%ticketurl
        else:
            avail_text =" unavailable"
            ticket_info="you can manually check %s"%ticketurl
        title="You have ticket becomes %s"%avail_text
        body="You have ticket becomes %s,  %s"%(avail_text,ticket_info)
        message=mail.EmailMessage(subject=title)
        message.sender = "Chen Jingmin <godosou@gmail.com>"
        message.bcc=recepients
        message.body=body
        message.send()
class ViewClients(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        clients=db.GqlQuery("SELECT * FROM Client")
        for client in clients:
            self.response.out.write('<div><b>%s</b>(%s)[%s]:%s</div>'%(client.name,client.email,client.adddate,client.ticketurl))
        self.response.out.write('</body></html>')
app = webapp2.WSGIApplication([('/',MainPage),
                               ('/addemail',AddEmail),
                               ('/showMatch',showMatch),
#                               ('/sendmail',sendmail),
                               ('/addMatch',addMatch),
#                               ('/viewclients',ViewClients),
#                               ('/changeTicketStatus',changeTicketStatus),
                               ('/showtickets',ShowTickets),
                               ('/checkticket',checkMatchTicketHandler)],debug=True)