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
        self.database_path = "postgresql://postgres:root@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "How are you ?", "answer": "i'm fine bro", "difficulty": 1, "category": 5}

            
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """ TODO
    Write at least one test for each test for successful operation and for expected errors.
    OK """

    # TEST (GET) ALL CATEGORIES
    # SUCCESS
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertTrue(len(data["categories"]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # TEST (GET) ALL QUESTIONS
    # SUCCESS
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(data["current_category"])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # TEST (GET) QUESTIONS BY CATEGORIES
    # SUCCESS
    def test_get_questions_by_categories(self):
        res = self.client().get("/categories/5/questions")
        data = json.loads(res.data)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # TEST (POST) CREATE NEW QUESTIONS
    # SUCCESS
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created (id)'])

    # TEST (DELETE) QUESTION BY ID
    # SUCCESS
    def test_delete_question(self):
        question_id = Question.query.order_by(Question.id.desc()).first().id # last record id
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == question_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted (id)'], question_id)
        self.assertEqual(question, None)

    # TEST (POST) SEARCH QUESTIONS WITH RESULTS
    # SUCCESS
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": ""})
        data = json.loads(res.data)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    # TEST (POST) SEARCH QUESTIONS WITHOUT RESULTS
    # SUCCESS (RETURNS 0 questions)
    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "blsnisonoisj"})
        data = json.loads(res.data)
        self.assertEqual(len(data["questions"]),0)
        self.assertEqual(data["total_questions"], 0)
        self.assertTrue(data["current_category"])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # TEST (GET) NEXT QUIZ QUESTION
    # SUCCESS
    def test_get_next_question_if_exist(self):
        previous_questions = [16,17,18]
        quiz_category = {'id': 2, 'type': "test"}
        res = self.client().post("/quizzes", json={"previous_questions": previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)
        self.assertTrue((data["question"]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # TEST (GET) NO MORE QUIZ QUESTION
    # SUCCESS (RETURNS 0 questions)
    def test_no_next_question(self):
        previous_questions = [16,17,18,19]
        quiz_category = {'id': 2, 'type': "test"}
        res = self.client().post("/quizzes", json={"previous_questions": previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)

    # TEST (DELETE) 422 delete question not processable
    # ERROR
    def test_422_unprocessable(self):
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # TEST (POST) BAD REQUEST
    # ERROR
    def test_400_bad_request(self):
        res = self.client().post("/questions", json={"invalidkey": "X"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # TEST (GET) QUESTIONS INVALID PAGES
    # ERROR
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # TEST (GET) INVALID CATEGORIES
    # ERROR
    def test_404_invalid_categories(self):
        res = self.client().get("/categories/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()