from django.conf.urls import url
from algebra.views import List, ExerciceCreation, AssessmentCreation, TrainingSession, APIExpressions, APIExpression

import API

urlpatterns = [
    url(r'^$', List.as_view(), name='list'),
    url(r'^exercice/creation$', ExerciceCreation.as_view(), name='exercice_creation'),
    url(r'^assessment/creation$', AssessmentCreation.as_view(), name='assessment_creation'),
    url(r'^student/training_session$', TrainingSession.as_view(), name='training_session_student'),
    url(r'^api/expressions', API.Expressions.as_view(), name='expressions'),
    url(r'^api/expression/(?P<id>[0-9]+)', API.Expression.as_view(), name='expression'),
    url(r'^api/expression', API.Expression.as_view(), name='expression'),
    url(r'^api/updated', API.Update.as_view(), name='update'),
]
