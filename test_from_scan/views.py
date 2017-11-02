# encoding: utf-8

import json
import qrtools
from datetime import datetime
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from PIL import Image
from skills.models import Skill, StudentSkill, SkillHistory
from examinations.models import TestFromScan, TestSkillFromScan

import os
from promotions.models import Lesson
from users.models import Student
from promotions.utils import user_is_professor, insertion_sort_file
from .forms import ImportCopyForm


@user_is_professor
def lesson_test_from_scan_add(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    return render(request, "professor/lesson/test/from-scan/add.haml", {
        "lesson": lesson,
        "stages": lesson.stages_in_unchronological_order(),
    })


@user_is_professor
def lesson_test_from_scan_detail(request, lesson_pk, pk):

    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=pk)
    print(test.content['a'][0]['y'][0])
    if request.method == "POST":
        print("POST")
        if 'copy' in request.FILES:
            print("FILES")
            form = ImportCopyForm(request.POST, request.FILES)
            if form.is_valid():
                copy = request.FILES.getlist('copy')
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)
                insertion_sort_file(copy)

                i = 1

                for c in copy:

                    img = Image.open(c)

                    qr = qrtools.QR()
                    qr.decode(c)


                    if int(qr.data)==1:
                        print("Page number 1 \n")
                        name = img.crop((797, 145, 1176, 189))
                        name.save(settings.SCAN_ROOT + "/name"+str(i)+".png")

                    for answer in test.content['a'][int(qr.data)-1]['y']:
                        print(answer)
                        img2 = img.crop((64, answer, 1175, answer+409))
                        img2.save(settings.SCAN_ROOT +"/crop" + str(i) + ".png")
                        i += 1


                return render(request, "professor/lesson/test/from-scan/detail.haml", {
                    "lesson": lesson,
                    "test":test,
                })
    else:
        return render(request, "professor/lesson/test/from-scan/detail.haml", {
            "lesson": lesson,
            "test":test,
        })


@user_is_professor
def lesson_test_from_scan_fill(request, lesson_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test_from_scan = get_object_or_404(TestFromScan, pk=pk)

    if request.method == "POST":
        second_run = []

        with transaction.atomic():
            for key in filter(lambda x: x.startswith(("good", "bad", "unknown")), request.POST.values()):
                result, student, skill = key.split("_", 2)
                student = Student.objects.get(pk=student)
                skill = Skill.objects.get(pk=skill)

                test_skill_from_scan, _ = TestSkillFromScan.objects.get_or_create(
                    test=test_from_scan,
                    student=student,
                    skill=skill,
                )

                test_skill_from_scan.result = result
                test_skill_from_scan.save()

                student_skill = StudentSkill.objects.get(
                    student=student,
                    skill=skill,
                )

                reasons = {
                    "who": request.user,
                    "reason": "Évaluation libre",
                    "reason_object": test_from_scan,
                }
                if result == "good":
                    student_skill.validate(**reasons)
                elif result == "bad":
                    student_skill.unvalidate(**reasons)

                second_run.append([result, student_skill])

            # I redo a second run here because we can end up in a situation where
            # the teacher has enter value that would be overwritten by the
            # recursive walk and we want the resulting skills to match the teacher
            # input
            for result, student_skill in second_run:
                if result not in ("good", "bad"):
                    continue

                if result == "good":
                    student_skill.acquired = datetime.now()
                elif result == "bad":
                    student_skill.acquired = None
                    student_skill.tested = datetime.now()

                SkillHistory.objects.create(
                    skill=student_skill.skill,
                    student=student_skill.student,
                    value="acquired" if result == "good" else "not acquired",
                    by_who=request.user,
                    reason="Évaluation libre (seconde passe)",
                    reason_object=test_from_scan,
                )

                student_skill.save()

        return HttpResponseRedirect(reverse('professor:lesson_test_from_scan_detail', args=(lesson.pk, test_from_scan.pk)))

    return render(request, "professor/lesson/test/from-scan/fill.haml", {
        "lesson": lesson,
        "test_from_scan": test_from_scan,
    })


@require_POST
@user_is_professor
def lesson_test_from_scan_add_json(request):
    # TODO: a professor can only do this on one of his lesson
    # TODO: use django form

    data = json.load(request)

    lesson = get_object_or_404(Lesson, id=data["lesson"])

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    with transaction.atomic():
        test = TestFromScan.objects.create(
            lesson=lesson,
            name=data["name"],
        )

        for skill_id in data["skills"]:
            test.skills.add(Skill.objects.get(code=skill_id))

        test.save()

    return HttpResponse(str(test.id))
