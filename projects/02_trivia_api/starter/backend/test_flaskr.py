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
        """
        Test success of endpoint /questions
        """

        res = self.client().get('/questions')
        res_json = res.get_json()

        self.assertEqual(res_json['success'], True)
        self.assertEqual(len(res_json['questions']), 10)

    def test_page_out_of_range(self):
        """
        Test success of endpoint /questions verifying error code if there is zero books in a page.
        """

        res = self.client().get('/questions?page=1000')
        res_json = res.get_json()

        self.assertEqual(res_json['success'], False)
        self.assertEqual(res_json['error'], 404)
        self.assertEqual(res_json['message'], 'not found')

    def test_delete_entry(self):
        """
        Test remove an entry from database.
        """

        questions = Question.query.all()
        question = questions[0]
        question_format = question.format()

        res = self.client().delete(f'/questions/{question_format["id"]}')
        res_json = res.get_json()

        self.assertEqual(res_json['success'], True)
        self.assertEqual(res_json['deleted_question']['id'], question_format["id"])

        # Add deleted question into database again
        new_question = Question(question_format['question'],
                                question_format['answer'],
                                question_format['category'],
                                question_format['difficulty'])

        new_question.insert()







# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()