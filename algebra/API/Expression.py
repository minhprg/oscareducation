
from __future__ import unicode_literals
from datetime import datetime
from itertools import chain
import inspect
import json
from collections import Sequence

from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse

from . import engine, engine_components, restify, AM

# Endpoint: '/algebra/api/expression[/<id>]?'
# Methods: ['GET', 'POST', 'PUT']
class Expression(View):
    """
    TODO
    """

    expression_dict_keys = [
        "expression",
        "type",
        "solution",
        "level"
    ]

    def _parse(self, e_json):
        """
        TODO
        """
        cls = e_json["type"].title().replace(" ", "")

        if not all(k in e_json.keys() for k in self.expression_dict_keys):
            raise ValueError("Missing information")
        if cls not in engine_components:
            raise ValueError("Unknown Expression type")

        cls = eval("engine." + cls)

        expression = cls(e_json["expression"])

        if expression.solution != e_json["solution"]:
            raise engine.ExpressionError("Incorrect expression solution")

        return expression

    def get(self, request, id):
        """
        TODO
        """
        try: expression = AM.objects.get(id=id)
        except ObjectDoesNotExist: return JsonResponse({}, status=404)

        return JsonResponse({
            'expression': model_to_dict(expression)
        }, status=200)

    def post(self, request):
        """
        TODO
        """
        try:
            e_json = json.loads(request.body)
            expression = self._parse(e_json)
        except (ValueError, engine.ExpressionError) as error:
            return JsonResponse({
                'reason': str(error)
            }, status=422)

        now = datetime.now()

        db_expression = AM(
            expression=str(expression),
            expression_type=expression._db_type,
            created=now,
            updated=now,
            solution=str(expression.solution),
            level=1 # TODO - dynamise
        )
        db_expression.save()

        return JsonResponse({
            'message': "Successfully created expression",
            'id': db_expression.id
        }, status=201)

    def put(self, request, id):
        """
        TODO
        """
        try:
            e_json = json.loads(request.body)
            expression = self._parse(e_json)
        except (ValueError, engine.ExpressionError) as error:
            return JsonResponse({
                'reason': str(error)
            }, status=422)

        try:
            db_expression = AM.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({
                'message': "Expression does not exist"
            }, status=404)

        db_expression.expression = str(expression)
        db_expression.expression_type = expression._db_type
        db_expression.updated = datetime.now()
        db_expression.solution = str(expression.solution)
        db_expression.save()

        return JsonResponse({}, status=204)
