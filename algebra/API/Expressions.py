# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from itertools import chain
import inspect
import json

from time import mktime, localtime
from datetime import datetime

from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse

from . import engine, engine_components, restify, AM

# Endpoint: '/algebra/api/expressions'
# Methods: ['GET']
class Expressions(View):
    """
    TODO
    """

    def get(self, request):
        """
        TODO
        """
        since = mktime(localtime(0)) * 1000
        try:
            rq = json.loads(request.body)
            if 'since' in rq.keys():
                since = float(rq['since'])
        except Exception: pass
        since = datetime.fromtimestamp(since)

        query_set = AM.objects.filter(updated__gte=since)
        ids = [expression.id for expression in query_set]
        print(ids)

        return JsonResponse({
            'ids': ids
        }, status=200)

    def post(self, request):
        since = None
        try:
            rq = json.loads(request.body)
            since = float(rq['since'])
        except Exception: return HttpResponse(status=422)
        since = datetime.fromtimestamp(since)

        query_set = AM.objects.filter(updated__gte=since)
        ids = [expression.id for expression in query_set]
        print(ids)

        return JsonResponse({
            'ids': ids
        }, status=200)
