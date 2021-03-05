import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app)

  @app.after_request
  def after_request(response):

    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():

    try:
      # get all categories by querying Category class.
      categories = Category.query.all()

      # Creating the dictionary to return
      categories_correlation = {category.id: category.type for category in categories}

    except:

      abort(500)

    return jsonify({'categories': categories_correlation,
                    'success': True,
                    'total_categories': len(categories_correlation)})



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  def get_question_per_page(request, questions):

    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    return questions[start:end]


  @app.route('/questions', methods=['GET'])
  def get_questions():

    questions = Question.query.all()
    current_questions = get_question_per_page(request, questions)

    current_questions_format = [question.format() for question in current_questions]

    # get all categories by querying Category class.
    categories = Category.query.all()

    # Creating the dictionary to return
    categories_correlation = {category.id: category.type for category in categories}
    
    current_categories = [question.get('category') for question in current_questions_format]

    return jsonify({'questions': current_questions_format,
                    'total_questions': len(questions),
                    'current_category': 'art',
                    'categories': categories_correlation,
                    'success':True
    })



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question_by_id(question_id):

    question = Question.query.filter(Question.id==question_id).one_or_none()

    #delete question persisting on database
    question.delete()

    return jsonify({'deleted_question': question.format(), 
                    'success':True
    })



  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():

    body = request.get_json()
    
    question =  body.get('question')
    answer =  body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')

    # Insert new question into database
    question = Question(question, answer, category, difficulty)

    # Persist data
    question.insert()

    questions = Question.query.all()
    current_questions = get_question_per_page(request, questions)

    current_questions_format = [question.format() for question in current_questions]

    return jsonify({'questions': current_questions_format,
                    'total_questions': len(questions),
                    'current_category': category})
                    

    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def return_search_result():

    body = request.get_json()
    
    search_term =  body.get('searchTerm')

    questions = Question.query.filter(Question.question.contains(search_term)).all()

    current_questions = get_question_per_page(request, questions)

    current_questions_format = [question.format() for question in current_questions]

    category=''

    return jsonify({'questions': current_questions_format,
                    'total_questions': len(questions),
                    'current_category': category})


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def get_questions_by_category_id(category_id):

    #include comment to test commit
    category_id = int(category_id)

    questions = Question.query.filter(Question.category==category_id).all()

    current_questions = get_question_per_page(request, questions)

    current_questions_format = [question.format() for question in current_questions]

    current_category = Category.query.filter(Category.id==category_id).one_or_none()

    return jsonify({'questions': current_questions_format,
                    'total_questions': len(questions),
                    'current_category': current_category.id})


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_question_to_play():

    body = request.get_json()
    
    previous_questions = body.get('previous_questions')
    quiz_category = body.get('quiz_category')

    # Select questions considering a specific category or ALL (can return any question from any category)
    category_id = quiz_category['id']

    if category_id == 0:
      
      questions = Question.query.all()

    else:

      questions = Question.query.filter(Question.category==int(category_id)).all()

    questions_format = [question.format() for question in questions]

    if isempty(questions_format):

      abort(404)

    new_question = random.choice(questions_format)

    # Avoid return repeated question
    while new_question['id'] in previous_questions:

      new_question = random.choice(questions_format)


    return jsonify({'success': True,
                    'question': new_question})



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  
  return app

    