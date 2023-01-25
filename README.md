# technopark_web_hw

Базалеев Фёдор группа WEB-13
задание https://github.com/ziontab/tp-tasks/


## параметры бд

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'askme',
        'USER': 'postgres',
        'PASSWORD': 'fedyk228',
        'HOST': 'localhost',
        'PORT': '',
    }
}

## команда для заполнения бд данными
python3 manage.py fill_db -ratio 100 , где 100 - кол-во пользователей
