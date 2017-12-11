
from __future__ import unicode_literals
from datetime import datetime
from itertools import chain
import inspect
import json

from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse

from . import engine_components, restify

# Endpoint: '/algebra/api/expression[/<id>]?'
# Methods: ['GET', 'POST', 'PUT']
class Pool(View):
    pass
