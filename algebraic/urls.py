from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^exercice/creation$', views.exercice_creation, name='exercice_creation'),
    url(r'^assessment/creation$', views.assessment_creation, name='assessment_creation'),
]
