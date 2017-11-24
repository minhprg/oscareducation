# -*- coding: utf-8 -*-

from django.http import JsonResponse, HttpResponse
from itertools import chain
import inspect

# ============================================================================
# =========================== Module dependencies ============================
# ============================================================================

import algebra.engine as engine
from algebra.models import AlgebraicExercice as AM

engine_components = list(chain(*[item for item in \
    inspect.getmembers(engine) if item[0] != "__builtins__"]))

def restify(func):
    """
    TODO
    """
    def restified(self, request, **kwargs):
        return func(self, request, **kwargs)
        #if request.content_type != "application/json":
        #    return HttpResponse(status=415)
    return restified

# ============================================================================

from Expressions import Expressions
from Expression import Expression
from Pool import Pool
from Update import Update
