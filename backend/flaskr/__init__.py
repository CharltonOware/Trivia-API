import sys, json
from random import randrange

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
    CORS(app, resources={r"/*":{"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods","GET,POST,PATCH,DELETE,OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        if categories is None:
            abort(404)
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({
            "success": True,
            "categories": formatted_categories
       })


    @app.route('/questions')
    def get_paginated_questions():
        selection = Question.query.order_by(Question.id).all()
        if selection is None:
            abort(404)
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()
        #store dictionary object having 'id': 'type' key:value pairs of the existing categories
        formatted_categories = {category.id: category.type for category in categories}
        
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "current_category": 'Sports',
            "categories": formatted_categories
        })

    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()

            questions = Question.query.all()
            current_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': current_questions
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
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        try:
            #If there is a search term, get all questions that meet the search term criteria
            if search:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
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
                }), 201
        except:
            print(sys.exc_info())
            abort(400)
            

    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(404)
        try:
            #convert category.id to string since it is defined as such in the Question model
            selection = Question.query.filter_by(category=str(category.id)).order_by(Question.id).all()
            current_questions = paginate_questions(request,selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category.type
            })
        except:
            print(sys.exc_info())
            abort(400)
            
    
    @app.route('/quizzes',methods=['POST'])
    def play_quiz():
        #get request parameters category & previous_question
        body = request.get_json()
        quiz_category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', [])
        #return randomized questions from within category if provided, and if not previous_question
        try:
            if quiz_category['id'] == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                print(quiz_category)#debugging line
                questions = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
            
            next_question = questions[randrange(len(questions))]

            if len(previous_questions) >= len(questions):
                res = jsonify({
                    "success": True,
                    "question": None
                })
            else:
                res = jsonify({
                    "success": True,
                    "question": next_question.format(),
                })
            print(res.json) #debugging line
            return res
        except:
            print(sys.exc_info())
            abort(400)
         

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

