import sys

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#Define helper function paginate_questions
def paginate_questions(request, selection):
    page = request.args.get('page',1,type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*":{"origins": "http://localhost:3000"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods","GET,POST,PATCH,DELETE")
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        if categories is None:
            abort(404)
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            "success": True,
            "categories": formatted_categories
        })


    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # """
    @app.route('/questions')
    def get_paginated_questions():
        selection = Question.query.order_by(Question.id).all()
        if selection is None:
            abort(404)
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()
        #formatted_categories = {category.format() for category in categories}
        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type
        
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "current_category": 'Sports',
            "categories": formatted_categories
        })

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'questions': list(Question.query.all())
            })
        except:
            print(sys.exc_info())
            abort(422)



    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
     """
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()
        search = body.get('searchTerm', None)
        new_question = body['question']
        new_answer = body['answer']
        new_category = body['category']
        new_difficulty = body['difficulty']
        try:
            #If there is a search term, get all questions that meet the search term criteria
            if search:
                selection = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(selection),
                        'current_category': ' '
                    })
            #If no search term provided, insert the provided question data into the DB and return new list of questions
            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection),
                    'current_category': ' '
                })
        except:
            abort(400)
            print(sys.exc_info())

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # """

    # """
    # @TODO:
    # Create a GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # """

    # """
    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500
    return app

