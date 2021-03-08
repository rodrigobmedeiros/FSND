import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user = "postgres"
        self.password = "draGao01"
        self.database_path = ''.join(['postgres', 
                                      '://',
                                      self.user,
                                      ':',
                                      self.password,
                                      '@',
                                      'localhost:5432',
                                      '/',
                                      self.database_name])


        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
        """
        Test success of endpoint /categories.
        """
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_get_question_success(self):
        pass



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()