from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.core.paginator import Paginator

per_page = 3

def paginate(objects_list, request, per_on_page=10):
    paginator = Paginator(objects_list, per_on_page)
    cur_page = request.GET.get('page')
    return paginator.get_page(cur_page)


def find_tag(id):
    for i in models.TAGS:
        if i['id'] == id:
            return 1
    return 0


def find_tag_in_qw(qw, id):
    tags = qw['tags']
    for i in tags:
        if i['id'] == id:
            return 1
    return 0

def find_qw_by_tag(id):
    res = []
    for i in models.QUESTIONS:
        if find_tag_in_qw(i, id):
            res.append(i)
    return res

from app.models import Question, Answer, Tag, Profile

def index(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    questions = Question.objects.get_questions_order_by_popularity()
    context = {'page': paginate(questions, request, per_page),
               'user': Profile.objects.all()[0],
               'popular_tags': tags,
               'popular_users': users,
               'is_full': False}
    return render(request, 'index.html', context=context)

def question(request, question_id: int):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    question_item = Question.objects.get_questions_by_id(question_id)
    if not question_item:
        return render(request, '404.html', status=404)

    context = {'question': question_item,
               'page': paginate(Answer.objects.get_answers(question_id), request, per_page),
               'is_full': True}
    return render(request, 'question.html', context=context)


def ask(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    return render(request, 'ask.html')


def settings(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    context = {'user': models.USER}
    return render(request, 'settings.html', context=context)


def tag(request, tag_id: int):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    tag_item = Tag.objects.get_tag_by_id(tag_id)
    if not tag_item:
        return render(request, '404.html', status=404)

    context = {'page': paginate(Question.objects.get_questions_by_tag(tag_id), request, per_page),
               'tag': tag_item}
    return render(request, 'tag.html', context=context)


def login(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    return render(request, 'login.html')


def register(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.get_all_users()[:5]

    return render(request, 'register.html')
