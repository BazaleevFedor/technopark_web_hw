from django.db import models
from random import randint

QUESTIONS = [
    {
        'id': question_id,
        'avatar': f'sea{question_id % 5}.jpg',
        'like_count': randint(1, 100),
        'title': f'Question #{question_id}',
        'text': f'Text of question #{question_id}',
        'full_text': f'Full text of question #{question_id}',
        'answers_count': question_id * 2,
        'answers': [
                    {
                        'id': answer_id,
                        'avatar': f'sea{answer_id % 5}.jpg',
                        'title': f'Question #{answer_id}',
                        'text': f'Text of answer #{answer_id}',
                        'like_count': randint(1, 100),
                        'is_correct': False,
                    } for answer_id in range(question_id * 2)],
        'tags': ['tag' for i in range(question_id)]
    } for question_id in range(100)
]

USER = {'name': 'Users Name',
        'avatar': 'sea4.jpg'}

TEGS = {
    'tag': QUESTIONS
}