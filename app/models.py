from django.db import models
from random import randint

QUESTIONS = [
    {
        'id': question_id,
        'avatar': f'sea{question_id % 5}.jpg',
        'like_count': randint(1, 100),
        'title': f'Question #{question_id}',
        'text': f'Text of question #{question_id}',
        'answers_count': question_id * 2,
        'tags': ['tag' for i in range(question_id)]
    } for question_id in range(10)
]

USER = {'name': 'Users Name'}
