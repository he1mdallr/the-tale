# coding: utf-8

from django.db import models

class WORD_TYPE:
    NOUN = 1
    ADJECTIVE = 2
    VERB = 3
    NUMERAL = 4
    NOUN_GROUP = 5
    FAKE = 6

WORD_TYPE_CHOICES = ( (WORD_TYPE.NOUN, u'существительное'),
                      (WORD_TYPE.ADJECTIVE, u'прилагательное'),
                      (WORD_TYPE.VERB, u'глагол'),
                      (WORD_TYPE.NUMERAL, u'числительное'),
                      (WORD_TYPE.NOUN_GROUP, u'группа существительного'),
                      (WORD_TYPE.FAKE, u'подделка') )


class Word(models.Model):

    normalized = models.CharField(max_length=32, unique=True, db_index=True)

    type = models.IntegerField(choices=WORD_TYPE_CHOICES)

    forms = models.TextField()

    properties = models.CharField(max_length=16)


class Template(models.Model):

    type = models.CharField(null=False, max_length=64, db_index=True)
    
    data = models.TextField(null=False, default='')