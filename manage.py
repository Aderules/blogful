import os
from flask.ext.script import Manager

from blog import app

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
    
    
from blog.database import session, Entry

@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
               Ut enim ad minim veniam, quis nostrud exercitation ullamo laboris nisi ut aliquip ex ea commode consequat.Duis aute irure dolor in 
               reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidate non proident, sunt in 
               culpa qui deserunt mollit amim id est laborum"""
    
    for i in range(25):
        entry = Entry(
            title="Test Entry #{}". format(i), 
            content=content
        )
    
if __name__=="__main__":
    manager.run()