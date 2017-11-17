from django.conf.urls import url
from algebra.views import List, ExerciceCreation, AssessmentCreation, TrainingSession, APIExpressions, APIExpression

urlpatterns = [
    url(r'^$', List.as_view(), name='list'),
    url(r'^exercice/creation$', ExerciceCreation.as_view(), name='exercice_creation'),
    url(r'^assessment/creation$', AssessmentCreation.as_view(), name='assessment_creation'),
    url(r'^student/training_session$', TrainingSession.as_view(), name='training_session_student'),

    url(r'^api/expressions', APIExpressions.as_view(), name='expressions'),
    url(r'^api/expression/(?P<id>[0-9]+)', APIExpression.as_view(), name='expression'),
]
