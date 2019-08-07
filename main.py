import webapp2
import jinja2
import os
from models import Meme 
from google.appengine.api import users


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class HomeHandler(webapp2.RequestHandler):
    def get(self):  # for a get request
        welcome_template = the_jinja_env.get_template('templates/home.html')
        self.response.write(welcome_template.render())

    def post(self):
        meme = Meme(
            line1=self.request.get('user-first-ln'), 
            line2=self.request.get('user-second-ln'), 
            img_choice=self.request.get('meme-type')
        )
        meme_key = meme.put()
        self.response.write("Meme created: " + str(meme_key) + "<br>")
        self.response.write("<a href='/allmemes'>All memes</a>")
        


class AllMemesHandler(webapp2.RequestHandler):
    def get(self):
        
        all_memes = Meme.query().fetch()
        
        the_variable_dict = {
            "all_memes": all_memes
        }
        
        all_memes_template = the_jinja_env.get_template('templates/all_memes.html')
        self.response.write(all_memes_template.render(the_variable_dict))
        
            
    
app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/allmemes', AllMemesHandler)
], debug=True)