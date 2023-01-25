from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from . import models
from django.core.paginator import Paginator

from .forms import LoginForm, RegistrationForm

per_page = 5

def paginate(objects_list, request, per_on_page=10):
    paginator = Paginator(objects_list, per_on_page)
    cur_page = request.GET.get('page')
    return paginator.get_page(cur_page)

from app.models import Question, Answer, Tag, Profile

def index(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    questions = Question.objects.get_questions_order_by_popularity()
    context = {'page': paginate(questions, request, per_page),
               'user': Profile.objects.all()[0],
               'popular_tags': tags,
               'popular_users': users,
               'is_full': False}
    return render(request, 'index.html', context=context)

def question(request, question_id: int):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    question_item = Question.objects.get_questions_by_id(question_id)
    if not question_item:
        return render(request, '404.html', status=404)

    context = {'question': question_item,
               'page': paginate(Answer.objects.get_answers(question_id), request, per_page),
               'popular_tags': tags,
               'popular_users': users,
               'is_full': True}
    return render(request, 'question.html', context=context)


def ask(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    context = {'popular_tags': tags,
               'popular_users': users,
               }

    return render(request, 'ask.html', context=context)


def settings(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    context = {'user': Profile.objects.all()[0],
               'popular_tags': tags,
               'popular_users': users,
               }
    return render(request, 'settings.html', context=context)


def tag(request, tag_id: int):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    tag_item = Tag.objects.get_tag_by_id(tag_id)
    if not tag_item:
        return render(request, '404.html', status=404)

    context = {'page': paginate(Question.objects.get_questions_by_tag(tag_id), request, per_page),
               'tag': tag_item,
               'popular_tags': tags,
               'popular_users': users,
               }
    return render(request, 'tag.html', context=context)


def login(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    print(request.GET)
    print(request.POST)
    msg =""

    if request.method == 'GET':
        user_form = LoginForm()

    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error='error: wrong password or username')

    context = {'form': user_form,
               'popular_tags': tags,
               'popular_users': users,
               }
    return render(request, 'login.html', context=context)


def register(request):
    tags = Tag.objects.get_questions_order_by_popularity()
    users = Profile.objects.all()[:5]

    print(request.GET)
    print(request.POST)

    if request.method == 'GET':
        user_form = RegistrationForm()

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request, **user_form.cleaned_data)
            if user:
                user_form.add_error(field=None, error='error: user already exists')
            else:
                user = user_form.save()
                if user:
                    return redirect(reverse('index'))
                else:
                    user_form.add_error(field=None, error='error: register error')

    context = {'form': user_form,
               'popular_tags': tags,
               'popular_users': users,
               }
    return render(request, 'register.html', context=context)
