import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    
    """ @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    OK """
    CORS(app, resources={r"/api/*": {"origins": "*"}})
   
    """ @TODO: Use the after_request decorator to set Access-Control-Allow
    OK """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """ @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    OK """
    @app.route("/categories", methods=['GET'])
    def retrieve_categories():

        categories_list = [category.format2() for category in Category.query.all()] # format2 is defined in models.py

        categories = {}
        for category in categories_list:
            categories.update(category)

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": categories,
                # "total_categories": len(Category.query.all())
            }
        )


    """ @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    OK """
    @app.route("/questions", methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)
        categories_query = retrieve_categories().get_json('categories')
        categories = categories_query['categories']
        

        if not len(questions):
            abort(404)
        else:
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(selection),
                    "categories": categories,
                    "current_category" : list(categories.items())[0][1] # get the value of the first element (in case categorie id 1 doesnt exist)
                }
        )


    """ @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    OK """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted (id)": question_id
                }
            )

        except:
            abort(422)

    """ @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    OK """
    @app.route("/questions", methods=['POST'])
    def create_or_search_question():
        body = request.get_json()
        post_body = json.loads(json.dumps(body))

        if all(key in post_body for key in ("question", "answer","difficulty","category")):
            NQ_q = body.get("question", None)
            NQ_a = body.get("answer", None)
            NQ_d = body.get("difficulty", None)
            NQ_c = body.get("category", None)
            if (NQ_q and NQ_a) and (NQ_d and NQ_c):
                question = Question(question=NQ_q,answer=NQ_a,difficulty=NQ_d,category=NQ_c)
                question.insert()
                return jsonify({
                    "success": True,
                    "created (id)": question.id
                })
            else: abort(422)
    # """ @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # OK """
        # if there is actually a search_tearm key
        if "searchTerm" in post_body:
            search_term = body.get("searchTerm")
            if search_term: #if search_term has a value
                selection = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
                questions = paginate_questions(request, selection)
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions": len(questions),
                    "current_category": Category.query.first().type

                })
            else: #if search_term exists but has no value
                return retrieve_questions()
        else: # if there is nothing
            abort(400)


    """ @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    OK """
    @app.route("/categories/<int:categorie_id>/questions")
    def questions_by_categories(categorie_id):
        selection = Question.query.filter(Question.category == categorie_id).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": questions,
                "total_questions": len(selection),
                "current_category" : Category.query.get(categorie_id).type
            }
        )


    """ @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    OK """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category_id = body.get('quiz_category')["id"]

        if category_id != 0: # if current category is not ALL
            selectionById = Question.query.filter(Question.category == category_id).filter(~Question.id.in_(previous_questions)).all()
            
            if selectionById :
                liste = [question.format() for question in selectionById]
                # random questions
                question = random.choice(liste)
                return jsonify({
                    'success': True,
                    'question': question
                })
            else:
                return jsonify({"success":True})
        else: # if current category is ALL
            selectionFromAll = Question.query.filter(~Question.id.in_(previous_questions)).all()
            if selectionFromAll :
                liste = [question.format() for question in selectionFromAll]
                # random questions
                question = random.choice(liste)
                return jsonify({
                    'success': True,
                    'question': question
                })
            else:
                return jsonify({"success":True})


        


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app

