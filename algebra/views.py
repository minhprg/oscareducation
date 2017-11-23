# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from datetime import datetime

from django.views import View

import json

from algebra.engine import Expression, ExpressionError, Equation, Inequation, EquationSystem
from algebra.models import AlgebraicExercice
from random import choice


# Create your views here.

class List(View):

    def get(self, request):
        expressions = AlgebraicExercice.objects.all()
        context = {
            'expressions': [expression.__dict__ for expression in expressions]
        }
        return TemplateResponse(request, "algebra/list.haml", context)

class TrainingSession(View):

    def get(self, request):
	print "test3"
	expressions = AlgebraicExercice.objects.filter(level=1)

	number = expressions.count()

	i=0
	tab = []
	while i!=number and i<10 :
		print "test4"
		myrandom = choice(range(0, number))
		while myrandom in tab:
			print tab
			myrandom = choice(range(0, number))
			print myrandom
		tab.append(myrandom)
		i+=1
	print tab

	i=0
	TabExpressions = []
	for expression in expressions:
		if i in tab:
			print i
			TabExpressions.append(expression)
		i+=1

        context = {
            'expressions': TabExpressions
        }
        return TemplateResponse(request, "algebra/training_session_student.haml", context)


    def _parse(self, json):

        if not all(k in json.keys() for k in ("expression",
            "type", "solution", "level")):
            raise ValueError()
        if json["type"] not in globals().keys():
            raise ValueError()

        expr = globals()[json["type"].title().replace(" ", "")](
            json["expression"]
        )

        solution = globals()[json["type"].title().replace(" ", "")](
            json["solution"]
        )

        if (expr.solution != solution.solution):
            raise ExpressionError()

        return expr, solution

    def post(self, request):
        if request.content_type != "application/json":
            return HttpResponse(status=415)

        try:

            expr, solution = self._parse(json.loads(request.body))
            print expr
            print solution
            #AlgebraicExercice.objects.all().delete()
            expressions = AlgebraicExercice.objects.filter(expression=expr)

            if str(expressions[0].solution)==str(solution) :
                return JsonResponse({
                    'status': True,
                    'message': "Ok-solution"
                }, status=200)

            return JsonResponse({
                'status': True,
                'message': "Ok"
            }, status=200)

        except ValueError as e:

            return JsonResponse({
                'status': False,
                'message': 'Malformé'
            }, status=422)

        except ExpressionError as e:

            return JsonResponse({
                'status': False,
                'message': 'mauvaise solution'
            }, status=422)


class ExerciceCreation(View):

    def _parse(self, json):

        if not all(k in json.keys() for k in ("expression",
            "type", "solution", "level")):
            raise ValueError()
        if json["type"] not in globals().keys():
            raise ValueError()

        expr = globals()[json["type"].title().replace(" ", "")](
            json["expression"]
        )

        solution = globals()[json["type"].title().replace(" ", "")](
            json["solution"]
        )

        if (expr.solution != solution.solution):
            raise ExpressionError()

        return expr, solution

    def get(self, request):

        if request.content_type is "application/json":
            return HttpResponse(status=415)
        else:
            return TemplateResponse(request, "algebra/exercice_creation.haml")

    def post(self, request):

        if request.content_type != "application/json":
            return HttpResponse(status=415)

        try:

            expr, solution = self._parse(json.loads(request.body))
            created = datetime.now()
            db_expr = AlgebraicExercice(
                expression=str(expr),
                expression_type=expr._db_type,
                created=created,
                updated=created,
                solution=str(solution),
                level=1
            )
            testExist = AlgebraicExercice.objects.filter(expression=str(expr))
            i = 0
            for elem in testExist :
                i+=1
            if i>0 :
                return JsonResponse({
                    'status': True,
                    'message': "Exercice déjà enregistré"
                }, status=200)
            else :
                db_expr.save()

            return JsonResponse({
                'status': True,
                'message': "Ok"
            }, status=200)

        except ValueError as e:

            return JsonResponse({
                'status': False,
                'message': 'Malformed or incomplete request body'
            }, status=422)

        except ExpressionError as e:

            return JsonResponse({
                'status': False,
                'message': 'Malformed algebraic expression or solution'
            }, status=422)


class AssessmentCreation(View):

    def get(self, request):
        return TemplateResponse(request, "algebra/assessment_creation.haml")


class APIExpressions(View):

    def get(self, request):
        query_set = AlgebraicExercice.objects.values_list('id', flat=True)
        ids = [id for id in query_set]

        return JsonResponse({
            'nb': ids
        }, status=200)

class APIExpression(View):

    def get(self, request, id):
        expr = {}

        try:
            expr = AlgebraicExercice.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({}, status=404)

        expr = model_to_dict(expr)
        return JsonResponse({
            'expression': expr
        }, status=200)
