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
from examinations.models import TestFromScan, TestSkillFromScan, TestAnswerFromScan, TestQuestionFromScan

import os
from promotions.models import Lesson, Students
from users.models import Student
from promotions.utils import user_is_professor, insertion_sort_file, all_different
from .forms import ImportCopyForm

@user_is_professor
def lesson_test_from_scan_match(request, lesson_pk, pk):

    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=pk)

    names = TestAnswerFromScan.objects.all().filter(test_id=pk).values('reference_name','student_id').distinct().order_by('reference_name')
    answers = TestAnswerFromScan.objects.all().filter(test_id=pk).order_by('id')

    nb_not_match = TestAnswerFromScan.objects.filter(student_id__isnull=True).count()
    nb_questions = TestQuestionFromScan.objects.filter(test_id=pk).count()

    flash_error = ""

    if nb_not_match == 0:
        flash_error = "Vous avez déjà associé tous les étudiants pour ce test, mais vous pouvez toujours remodifier la totalité"

    if request.method == "POST":
        form = request.POST.getlist('students')
        if all_different(form):
            i = 0
            question_count = 0
            for student in form:
                for answer in range(i, len(answers)):
                    print(student)
                    TestAnswerFromScan.objects.filter(pk=answers[answer].id).update(student_id=student)
                    i+=1
                    question_count +=1
                    if question_count >= nb_questions:
                        question_count=0
                        break

        else:
            flash_error = "Un élève ne peut pas être associé deux fois"

        return HttpResponseRedirect('/professor/lesson/'+str(lesson_pk)+'/test/from-scan/'+str(pk)+'/match/')

    return render(request, "professor/lesson/test/from-scan/match.haml", {
        "lesson": lesson,
        "test": test,
        "names": names,
        "answers": answers,
        "flash": flash_error,
        "nb_not_match":nb_not_match,
    })

@user_is_professor
def lesson_test_from_scan_correct_one(request, lesson_pk, test_pk, pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=test_pk)
    answer = get_object_or_404(TestAnswerFromScan, pk=pk)

    if answer.annotation == None:
        answer.annotation = ""

    if request.method == "POST":
        correction = request.POST.get('correction')
        annotation = request.POST.get('annotation')

        if correction == "1" or correction == "0":
            if not annotation:
                annotation = None
            TestAnswerFromScan.objects.filter(pk=pk).update(is_correct=correction, annotation=annotation)
        return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/from-scan/' + str(test_pk) + '/correct/' + str(pk))
    return render(request, "professor/lesson/test/from-scan/correct_one.haml", {
        "lesson": lesson,
        "test": test,
        "answer":answer,
    })


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
    answers = TestAnswerFromScan.objects.all().filter(test_id=pk).order_by('id')
    questions = TestQuestionFromScan.objects.all().filter(test_id=pk).order_by('question_num')


    if request.method == "POST":
        if 'copy' in request.FILES:
            form = ImportCopyForm(request.POST, request.FILES)
            if form.is_valid():
                copy = request.FILES.getlist('copy', False)

                if not os.path.isdir(settings.STATIC_ROOT +"/tests/"+pk) and copy:
                    os.makedirs(settings.STATIC_ROOT +"/tests/"+pk)

                insertion_sort_file(copy)

                last_answer = TestAnswerFromScan.objects.order_by('-id')
                if (len(last_answer) == 0):
                    i = 1
                else:
                    i = last_answer[0].id
                count_question = 0
                for c in copy:

                    img = Image.open(c)

                    qr = qrtools.QR()
                    qr.decode(c)

                    if int(qr.data)==1:
                        print("Page number 1 \n")
                        name = img.crop((797, 145, 1176, 189))
                        ref_name = "/tests/"+ pk + "/name"+str(i)+".png"
                        name.save(settings.STATIC_ROOT +"/tests/"+ pk + "/name"+str(i)+".png")
                        count_question = 0

                    for answ in test.content['a'][int(qr.data)-1]['y']:
                        answer = TestAnswerFromScan(test_id=pk, question_id=questions[count_question].id, reference_name=ref_name, reference='/tests/'+pk+'/crop'+str(i)+'.png')
                        answer.save()
                        img2 = img.crop((64, answ, 1175, answ+409))
                        img2.save(settings.STATIC_ROOT +"/tests/"+ pk + "/crop" + str(i) + ".png")
                        i += 1
                        count_question +=1
        return HttpResponseRedirect('/professor/lesson/'+str(lesson_pk)+'/test/from-scan/'+str(pk)+'/')

    return render(request, "professor/lesson/test/from-scan/detail.haml", {
        "lesson": lesson,
        "test":test,
        "answers":answers,
        "questions": questions,
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
