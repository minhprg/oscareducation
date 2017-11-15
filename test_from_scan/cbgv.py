from django.views.generic import DetailView
from examinations.models import TestFromScan

from promotions.cbgv import LessonMixin


class TestFromScanDetailView(LessonMixin, DetailView):
    model = TestFromScan
    template_name = "professor/lesson/test/from-scan/detail.haml"
