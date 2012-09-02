'''
Created on Aug 29, 2012

@author: jchen
'''
import webapp2
from google.appengine.ext import db
class Match(db.Model):
    """Models client's email"""
    url = db.LinkProperty()
    name=db.StringProperty()
    description=db.StringProperty(multiline=True)
def putMatchToDB(name, url,description):
    match=Match()
    match.name=name
    match.url=url
    match.description=description
    match.put()

class addMatch(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        url = self.request.get('url')
        description = self.request.get('description')
        existing_requests=Match.all()
        existing_requests.filter('url=',url)
        existing_requests.fetch(1)
        
        flag=True
        for req in existing_requests:
            flag=False
        if flag:
            putMatchToDB(name,url,description)
        self.redirect('/showMatch')
class showMatch(webapp2.RequestHandler):    
    def get(self):
        self.response.headers['Content-Type']='text/html'  
        q=Match.all() 
        results=q.fetch(10000)
        self.response.out.write("<div>")
        for r in results:
            self.response.out.write("<div>%s: %s. %s</div>"%(r.name,r.description,r.url))
        self.response.out.write("</div>")
      
        self.response.out.write("""
          <html>
            <body>
            <h1>Add match info</h1><br/>
              <form action="/addMatch" method="post">
                <div><lable>Name:</label><input name="name" type="text"></input></div>
                <div><lable>Url:</label><input name="url" type="text"></input></div>
                <div><lable>Description:</label><textarea name="description"  rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="Add Match"></div>
              </form>
            </body>
          </html>""")
