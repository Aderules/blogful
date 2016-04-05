import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

#Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"


from blog import app
from blog.database import Base, engine, session, User, Entry
from flask import flash

class TestViews(unittest.TestCase):
    def setUp(self):
        """Test setup """
        self.client = app.test_client()
        
        #Set up the tables in the database
        Base.metadata.create_all(engine)
        
        #Create an example user
        self.user = User(name="Alice", email="alice@example.com", password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()
        
    def stimulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True
    
    def test_add_entry(self):
        self.stimulate_login()
        
        response = self.client.post("/entry/add", data={"title": "Test Entry", "content": "Test content"})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)
        
    def test_edit_entry(self):
        #Check that entries can be edited
        self.stimulate_login()
        #create test entry
        response = self.client.post("/entry/add", data={"title": "Test Entry", "content": "Test content"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        #edit entry
        response = self.client.post("/entry/1/edit", data={"title": "Test Edit Entry", "content": "Test Edit content"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        
       #test entry is edited
        self.assertEqual(entry.author,self.user)
        self.assertEqual(entry.title,"Test Edit Entry")
        self.assertEqual(entry.content, "Test Edit content")
        self.assertEqual(entry.id, 1)
        
   # def test_edit_unauthorised_entry(self):
       # self.stimulate_login("Bob")
        
        #response = self.client.post("/entry/1/edit", data={"title": "Test Edit Entry", "content": "Test Edit content"})
       # self.assertEqual(response.status_code, 403)
       
    
    def test_authorised_delete_entry(self):
       self.stimulate_login()
       #add entry
       response = self.client.post("/entry/add", data={"title": "Test Entry", "content": "Test content"})
       #self.assertEqual(response.status_code, 302)
      # self.assertEqual(urlparse(response.location).path, "/")
      
       #confirm entry has been added
       entries = session.query(Entry).all()
       entry=entries[0]
       #self.assertEqual(len(entries), 1)
       self.assertEqual(entry.author, self.user) 
      #delete entry
       response = self.client.post("/entry/1/delete")
       self.assertEqual(response.status_code, 302)
       entries = session.query(Entry).all()
       self.assertEqual(len(entries), 0)
       
    
      # self.assertEqual(entry.title, "[]")
      # self.assertEqual(entry.content, "[]")
       
      

    
    def tearDown(self):
        """ Test teardown """
        session.close()
        #Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
if __name__ == "__main__":
    unittest.main()