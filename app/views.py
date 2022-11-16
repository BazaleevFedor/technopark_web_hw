from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.core.paginator import Paginator


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    cur_page = request.GET.get('page')
    return paginator.get_page(cur_page)


def index(request):
    questions = models.QUESTIONS
    context = {'page': paginate(questions, request, 3),
               'user': models.USER,
               'is_full': False}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    if question_id >= len(models.QUESTIONS):
        return render(request, '404.html', status=404)

    question_item = models.QUESTIONS[question_id]
    context = {'question': question_item,
               'page': paginate(question_item['answers'], request, 3),
               'is_full': True}
    return render(request, 'question.html', context=context)


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    context = {'user': models.USER}
    return render(request, 'settings.html', context=context)


def tag(request, tag_name: str):
    if (tag_name not in models.TEGS) or (int(request.GET.get('page'))*3 - 3 > len(models.TEGS[tag_name])):
        return render(request, '404.html', status=404)

    context = {'page': paginate(models.TEGS[tag_name], request, 3),
               'tag': tag_name}
    return render(request, 'tag.html', context=context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
