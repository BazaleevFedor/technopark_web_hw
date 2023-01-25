from django.contrib.auth.models import User
from django.db import models


class ProfileManager(models.Manager):
    def get_all_users(self):
        return self.all()


class Profile(User):
    avatar = models.FileField(upload_to='static/img/')

    objects = ProfileManager()

class TagManager(models.Manager):
    def get_questions_order_by_popularity(self):
        return self.order_by('questions')[:5]

    def get_tag_by_id(self, _id):
        if self.filter(pk=_id):
            return self.filter(pk=_id)[0]

class Tag(models.Model):
    name = models.CharField(max_length=30)

    objects = TagManager()

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def get_questions_order_by_popularity(self):
        return self.all().order_by('-likes')

    def get_questions_order_by_date(self):
        return self.all().order_by('id')

    def get_questions_by_id(self, _id):
        if self.filter(pk=_id):
            return self.filter(pk=_id)[0]

    def get_questions_by_tag(self, _id):
        return self.filter(tags__id=_id).order_by('id')


class Question(models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=300)
    likes = models.IntegerField()
    tags = models.ManyToManyField(Tag, verbose_name='tags', related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.text

    def answers_count(self):
        return Answer.objects.filter(question__id=self.pk).count()

    def get_avatar(self):
        return Profile.objects.filter(profile__id=self.pk)[0]


class AnswerManager(models.Manager):
    def get_answers(self, _id):
        return self.filter(question__pk=_id)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=300)
    correct = models.BooleanField()
    likes = models.IntegerField()

    objects = AnswerManager()

    def __str__(self):
        return self.text


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
