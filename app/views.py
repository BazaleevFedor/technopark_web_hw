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

def index(request):
    questions = models.QUESTIONS
    context = {'page': paginate(questions, request, per_page),
               'user': models.USER,
               'is_full': False}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    if question_id >= len(models.QUESTIONS):
        return render(request, '404.html', status=404)

    question_item = models.QUESTIONS[question_id]
    context = {'question': question_item,
               'page': paginate(question_item['answers'], request, per_page),
               'is_full': True}
    return render(request, 'question.html', context=context)


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    context = {'user': models.USER}
    return render(request, 'settings.html', context=context)


def tag(request, tag_id: int):
    if not find_tag(tag_id):
        return render(request, '404.html', status=404)

    context = {'page': paginate(find_qw_by_tag(tag_id), request, per_page),
               'tag': models.TAGS[tag_id]['name']}
    return render(request, 'tag.html', context=context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
