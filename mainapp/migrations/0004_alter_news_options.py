# Generated by Django 4.1.2 on 2022-10-06 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_courses_alter_news_preamble_subnews_lesson_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-create_date',), 'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
    ]
