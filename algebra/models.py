# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AlgebraicExercice(models.Model):

    TYPES = (
        ('EQ', 'Equation'),
        ('IN', 'Inequation'),
        ('ES', 'EquationSystem')
    )

    expression                  = models.CharField(max_length=60)
    expression_type = models.CharField(max_length=2, choices=TYPES)
    created                     = models.DateField()
    updated                     = models.DateField()
    solution                    = models.CharField(max_length=30)
    level                       = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'algebraic_expression'

