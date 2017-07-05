# -*- coding:utf-8 -*-

import logging
import datetime

from django.db import models

logger = logging.getLogger('data')

class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="full name")
    age = models.IntegerField( verbose_name="age")
    test = models.DateTimeField(default=datetime.datetime.now, verbose_name="age")

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class meta:
        db_name = 'example_app_blog'

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    class meta:
        db_name = 'example_app_author'

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()
    status = models.IntegerField(choices=(
        (0, "Draft"),
        (1, "Published"),
    ))

    class meta:
        db_name = 'example_app_entry'
