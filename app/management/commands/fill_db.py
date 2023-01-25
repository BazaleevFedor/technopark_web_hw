from django.core.management.base import BaseCommand

from app.models import Profile, Tag, Question, QuestionLike, Answer, AnswerLike
from random import choice, sample, randint
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Fill DataBase Python'

    def add_arguments(self, parser):
        parser.add_argument('-ratio', type=int)
        parser.add_argument('-questions', type=int)

    def handle(self, *args, **options):
        if options['ratio']:
            self.fill_db(options['ratio'])

        if options['questions']:
            self.fill_questions(options['questions'])

        self.stdout.write(self.style.SUCCESS('Data creation was successful'))

    @staticmethod
    def fill_profiles(n, avatar_n=5):
        for i in range(n):
            Profile.objects.create(username=faker.user_name(), email=faker.email(),
                                   password=faker.password(), avatar="static/img/sea" + str(i % avatar_n) + ".jpg")

    @staticmethod
    def fill_tags(n):
        for i in range(n):
            Tag.objects.create(name=faker.word())

    @staticmethod
    def fill_questions(n, max_tags=10):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        for i in range(n):
            try:
                tags_list = sample(tag_ids, randint(1, max_tags))
                profile_item = Profile.objects.get(pk=choice(profile_ids))
                Question.objects.create(
                    title=faker.sentence(10),
                    text=faker.sentence(200),
                    profile=profile_item,
                    likes=0,
                ).tags.set(tags_list)
            except Exception:
                print(profile_item, tags_list)
                pass

    @staticmethod
    def fill_answers(n):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))
        statuses = [0, 1]
        for i in range(n):
            try:
                Answer.objects.create(
                    question=Question.objects.get(pk=choice(question_ids)),
                    text=faker.text(),
                    profile=Profile.objects.get(pk=choice(profile_ids)),
                    correct=choice(statuses),
                    likes=0,
                )
            except Exception:
                pass

    @staticmethod
    def fill_questions_likes(n):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))

        for i in range(n):
            try:
                like = QuestionLike(
                    question=Question.objects.get(pk=choice(question_ids)),
                    profile=Profile.objects.get(pk=choice(profile_ids)),
                )
                like.save()
            except Exception:
                print("err")
                pass

    @staticmethod
    def fill_answers_likes(n):
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        answer_ids = list(Answer.objects.values_list('id', flat=True))

        for i in range(n):
            try:
                like = AnswerLike(
                    answer=Answer.objects.get(pk=choice(answer_ids)),
                    profile=Profile.objects.get(pk=choice(profile_ids)),
                )
                like.save()
            except Exception:
                pass

    def fill_db(self, n):
        self.fill_profiles(n)
        self.fill_tags(n)
        self.fill_questions(n*10)
        self.fill_answers(n*100)
        self.fill_questions_likes(n*200)
        self.fill_answers_likes(n*200)
