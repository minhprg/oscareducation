from django.conf.urls import url
from algebra.views import List, ExerciceCreation, AssessmentCreation

urlpatterns = [
    url(r'^$', List.as_view(), name='list'),
    url(r'^exercice/creation$', ExerciceCreation.as_view(), name='exercice_creation'),
    url(r'^assessment/creation$', AssessmentCreation.as_view(), name='assessment_creation'),
    url(r'^student/training_session$', TrainingSession.as_view(), name='training_session'),
]
