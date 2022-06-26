import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import request
from dotenv import load_dotenv

from flaskr import create_app
from models import setup_db, Question, Category

#Grab folder where script runs
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,DB_HOST, self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question":"Who is the current manager of Manchester United?",
                                "answer":"Eric Ten Hag",
                                "category": 6,
                                "difficulty": 3}

        self.new_question_2 = {"question":"Who is the current manager of Manchester United?",
                                "answer":"ETH",
                                "category":  ' ',
                                "difficulty": 3}

        self.search_term = {"searchTerm": 'soccer'}

        self.alternative_search_term = {"searchTerm": 'elimi'}

        self.new_request = {"previous_questions": [1, 4, 20, 15],
                            "quiz_category": {"id": 2}
                            }
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_paginated_questions(self):
        """Test for getting all questions in the current page"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

    def test_404_requested_page_outside_range(self):
        """Test for a failed retrieval of questions due to
        page out of range
        """
        res = self.client().get('/questions?page=1000', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        """Test get all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # def test_delete_question_of_provided_id(self):
    #     """Test delete specific question"""
    #     res =self.client().delete('/questions/20')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'],True)
    #     self.assertTrue(data['questions'])
        

    def test_404_delete_question_if_not_exists(self):
        """Test failed delete of question which doesn't exist"""
        #Please alter the value below to run the test
        question_id = 400
        res = self.client().delete('/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'resource not found')
        self.assertEqual(question, None)

    def test_search_question(self):
        """Test search question based on provided search term"""
        res = self.client().post('/questions', json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_search_question_if_search_no_match(self):
        """Test search question where none matches the search term"""
        res = self.client().post('/questions', json=self.alternative_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["questions"], [])

    def test_insert_new_question(self):
        """Test successful addition of new question"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_400_if_question_creation_request_incorrect(self):
        """Test failed addition of new question due to bad request"""
        res = self.client().post('/questions', json=self.new_question_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'bad request')

    def test_filter_questions_by_category(self):
        """Test successful filter by category"""
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_if_category_not_exists(self):
        """Test failed filter when category doesn't exist"""
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    def test_filter_questions_by_category_if_no_questions(self):
        """Test returns empty list when all questions in the provided category had been deleted"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['questions'])
        
    def test_play_quiz(self):
        """Test successful submission of quiz"""
        res = self.client().post('/quizzes',json=self.new_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'],None)

    def test_400_if_quiz_posting_unsuccessful(self):
        """Test unsuccessful posting of quiz"""
        res = self.client().post('/quizzes', json={})
        data =json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()