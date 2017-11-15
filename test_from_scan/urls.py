from django.conf.urls import url

from promotions.utils import user_is_professor

import views

from .cbgv import TestFromScanDetailView


urlpatterns = [
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<pk>\d+)/fill/$', views.lesson_test_from_scan_fill, name='lesson_test_from_scan_fill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<pk>\d+)/download/$', views.lesson_test_from_scan_download, name='lesson_test_from_scan_download'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<pk>\d+)/match/$', views.lesson_test_from_scan_match, name='lesson_test_from_scan_match'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<test_pk>\d+)/correct/(?P<pk>\d+)$', views.lesson_test_from_scan_correct_one, name='lesson_test_from_scan_correct_one'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<test_pk>\d+)/student/(?P<pk>\d+)/correct/$', views.lesson_test_from_scan_correct_by_student, name='lesson_test_from_scan_correct_by_student'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<pk>\d+)/$', views.lesson_test_from_scan_detail, name='lesson_test_from_scan_detail'),
    url(r'^lesson/(?P<pk>\d+)/test/from-scan/add/$', views.lesson_test_from_scan_add, name='lesson_test_from_scan_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-scan/(?P<pk>\d+)/modify/$',
        user_is_professor(TestFromScanDetailView.as_view(template_name="professor/lesson/test/from-scan/exercices.haml")),
        name='lesson_test_from_scan_modify'),
    url(r'^add_test_from_scan_for_lesson/$', views.lesson_test_from_scan_add_json, name='lesson_test_from_scan_add_json'),

]
