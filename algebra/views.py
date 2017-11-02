# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.
def list(request):
    return TemplateResponse(request, "algebra/list.haml")

def exercice_creation(request):
    return TemplateResponse(request, "algebra/exercice_creation.haml")

def assessment_creation(request):
    return TemplateResponse(request, "algebra/assessment_creation.haml")
