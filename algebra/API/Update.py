
from __future__ import unicode_literals
from datetime import datetime
from itertools import chain
import inspect
import json
from time import localtime, mktime
from collections import Sequence

from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse

from . import engine, engine_components, restify, AM

# Endpoint: '/algebra/api/updated'
# Methods: ['GET']
class Update(View):

    def get(self, request):

        try: expression = AM.objects.latest('updated')

        except ObjectDoesNotExist: return JsonResponse({
            'date': mktime(localtime(0)) * 1000
        }, status=200)

        return JsonResponse({
            'date': mktime(expression.updated.timetuple()) * 1000
        }, status=200)
