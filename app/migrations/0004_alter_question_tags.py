# Generated by Django 4.1.3 on 2023-01-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_profile_managers_alter_answer_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', to='app.tag', verbose_name='tags'),
        ),
    ]