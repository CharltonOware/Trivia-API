# Trivia App
> How knowledgeable are you?

## Description

In this app, which consists of a flask-based REST API and a frontend developed in React, users will get to answer random questions within a category of choice (the categories are History, Science, Geography, Entertainment, Art and Sports). A user can also play without being specific about a category.

A user need not login to access the site.

The general interface of the web app is such that:

1. It displays questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. A user can delete questions.
3. A user can add questions with the requirement that they include question and answer text.
4. A user can search for questions based on a text query string. This string can be partial.
5. Play the quiz game, randomizing either all questions or within a specific category.

As a developer, completing this trivia app helps me demonstrate my ability to structure, plan, implement, and test an API as a completion requirement for my Udacity Full-stack web developer nanodegree.
## Technologies
Flask <br>
React <br>
Postgresql
## Contributing to the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before [Making a pull request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-a-pull-request).


## About the Stack

This full-stack application is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a completed API and its test file.
Migrations have not been implemented and would be a good starting point for a future contributor.
The models.py also has a database path defined, which assumes Postgresql will always be used. Feel free to use your preferred database engine.
You are advised to store your sensitive credentials in a local .env file.


> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend changes that you make. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Reference
### Getting started
-Base URL: This app is currently only run locally and is not hosted as a base URL. The backend app is hosted at `http://127.0.0.1:5000` that is set as a proxy in the frontend configuration. <br>
-Authentication: No authentication or API keys required in this version of the application

### Endpoints
`GET '/categories'`
- General:
    - Fetches a dictionary of all the categories with the key as 'id' and value as the corresponding string.
- Sample: `curl http://127.0.0.1:5000/categories`
- Request arguments: None
- Returns: An object with two keys 'categories' that contains an object of key: value pair `id: category_string` and 'success' that contains a boolean value 'True'.

```json
{
    "success": True,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```
`GET '/questions'`
- General
    - Fetches a paginated list of questions, the total number of all questions returned from the database, the current category, and the categories of the questions currently posted on the app.
- Sample `curl http://127.0.0.1:5000/questions?page=1`
- Request arguments: `page` - integer
- Returns an object with the keys "success", "questions", "total_questions", "current_category" and "categories" with values True, "paginated_list_of_10_formatted_questions", "count_of_items_returned_from_questions_table", "catgegory_string" and "dictionary with key 'id' and value 'category_string'" respectively

```json 
{
    "success": True,
    "questions": [
        {
           "id": 1,
           "question": "What boxer's original name is Cassius Clay?",
           "answer": "Muhammad Ali",
           "category": "History",
           "difficulty": 3
        },
        {
           "id": 2,
           "question": "How many paintings did Van Gogh sell in his lifetime?",
           "answer": "One",
           "category": "Art",
           "difficulty": 4
        },
        {
           "id": 3,
           "question": "Which is the only team to play in every soccer World Cup tournament?",
           "answer": "Brazil",
           "category": "Sports",
           "difficulty": 3
        }
        
    ],
    "total_questions": 3,
    "current_category": " ",
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports" 
    }

}
```

`DELETE '/questions/{question_id}'`
- General:
    - Deletes the question of given if it exists.
- Sample : `curl -X DELETE http://127.0.0.1:5000/questions/2?page=1`
- Request arguments: `question_id` - integer
- Returns an object of keys "success" and "questions" with values True and "list of questions based on current page number" respectively

```json
{
    "success": True,
    "questions": [
        {
           "id": 1,
           "question": "What boxer's original name is Cassius Clay?",
           "answer": "Muhammad Ali",
           "category": "History",
           "difficulty": 3
        },
        
        {
           "id": 3,
           "question": "Which is the only team to play in every soccer World Cup tournament?",
           "answer": "Brazil",
           "category": "Sports",
           "difficulty": 3
        }
    ]
}

```

`POST '/questions'`
- General : Creates a new question using the submitted question, answer, category and difficulty.
- Request body: 
```json
{
    "question": "New question",
    "answer": "Answer to new question",
    "category": "2",
    "difficulty": 3
}
```
- Sample: `curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"question": "How many paintings did Van Gogh sell in his lifetime?", "answer": "One", "category": "2", "difficulty": 4}'`
- Returns: An object with keys "success", "questions", "total_questions" and "current_category" with values True, list_of_paginated_questions, count_of_questions_in_the_table and a category string respectively.

```json
{
    "success": True,
    "questions": [
        {
           "id": 1,
           "question": "What boxer's original name is Cassius Clay?",
           "answer": "Muhammad Ali",
           "category": "History",
           "difficulty": 3
        },
        
        {
           "id": 3,
           "question": "Which is the only team to play in every soccer World Cup tournament?",
           "answer": "Brazil",
           "category": "Sports",
           "difficulty": 3
        }
    ],
    "total_questions": 3,
    "current_category": " "
}
```
`POST '/questions'`
- General: Searches for a question(s) that matches the searchterm provided in the request.
- Request body: 
```json
    "searchterm": "match this string"
```
- Returns: An object with keys "success", "questions", "total_questions" and "current_category" with values True, list_of_paginated_questions, count_of_questions_in_the_table and a category string respectively.

`GET '/categories/{category_id}/questions'`
- General: Fetches all questions that belong to the category of id provided
- Sample `curl http://127.0.0.1:5000/categories/5/questions`
- Returns an object of keys "success", "questions", "total_questions" and "current_category" with values True, paginated_list_of_questions, count_of_questions_of_selected_category and the current_category_string respectively

```json
{
    "success": True,
    "questions": [
        {
           "id": 1,
           "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
           "answer": "Apollo 13",
           "category": "Entertainment",
           "difficulty": 4
        },
        
        {
           "id": 3,
           "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
           "answer": "Tom Cruise",
           "category": "Entertainment",
           "difficulty": 4
        }
    ],
    "total_questions": 2,
    "current_category": "Entertainment"
}
```

`POST '/quizzes'`
- General: Fetches random questions depending on the selected category and then displays 'correct' or 'failed' depending on the player's answer. If all the questions in the category have been played, it returns a blank page.
- Request body :
```json
{
    "previous_questions": [1,3,15,6],
    "current_category": current_category
}
    
```
- Returns: An object with keys "success" and "question" with values True and a formatted question object respectively.

```json
{
    "success": True,
    "question": {
        "id": 1,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
        "answer": "Apollo 13",
        "category": "5",
        "difficulty": 4
    }
}
```
## Authors Info

Charlton Omondi, Udacity team,

## Acknowledgements

@udacity/active-public-content
