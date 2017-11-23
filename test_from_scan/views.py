# encoding: utf-8

import json
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
from examinations.models import TestFromScan, TestSkillFromScan, TestAnswerFromScan, TestQuestionFromScan, BaseTest
from django.contrib import messages
import os, tempfile, zipfile
from promotions.models import Lesson, Students
from users.models import Student
from promotions.utils import user_is_professor, insertion_sort_file, all_different, generate_pdf, generate_coordinates, pt_to_px, pdf2png
from .forms import ImportCopyForm
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.core.files.storage import default_storage




@user_is_professor
def lesson_test_from_scan_match(request, lesson_pk, pk):
    is_exist = TestAnswerFromScan.objects.filter(test_id=pk).count()
    nb_not_match = TestAnswerFromScan.objects.filter(student_id__isnull=True).count()
    if is_exist == 0:
        messages.error(request, "Importez un test avant de pouvoir associer vos élèves")
        return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/from-scan/' + str(pk) + '/')

    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=pk)

    names = TestAnswerFromScan.objects.all().filter(test_id=pk).values('reference_name','student_id').distinct().order_by('reference_name')
    answers = TestAnswerFromScan.objects.all().filter(test_id=pk).order_by('id')

    nb_not_match = TestAnswerFromScan.objects.filter(student_id__isnull=True).count()
    nb_questions = TestQuestionFromScan.objects.filter(test_id=pk).count()

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
            messages.success(request, "Modifications effectuées")
        else:
            messages.error(request, "Un étudiant ne peut pas être associé deux fois")

        return HttpResponseRedirect('/professor/lesson/'+str(lesson_pk)+'/test/from-scan/'+str(pk)+'/match/')
    return render(request, "professor/lesson/test/from-scan/match.haml", {
        "lesson": lesson,
        "test": test,
        "names": names,
        "answers": answers,
        "nb_not_match":nb_not_match,
    })

@user_is_professor
def lesson_test_from_scan_add(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == "POST":
        form = request.POST.items()

        title = request.POST.get('titre')

        scan = TestFromScan.objects.create(
            lesson = lesson,
            name = title,
        )
        skills = request.POST.get('skills-scan').split(",")
        for skill_id in skills:
            scan.skills.add(Skill.objects.get(code=skill_id))

        """for student in lesson.students.all():
            scan.add_student(student)"""


        try:
            scan.save()
        except Exception as e:
            messages.error(request, "Une erreur s'est produite durant la création.")
            return HttpResponseRedirect('/professor/lesson/'+str(pk)+'/test/from-scan/add/')

        form = sorted(form, key=lambda tup: tup[0])
        print(form)
        file = generate_pdf(form,scan.id)

        content = generate_coordinates(file)

        try:

            TestFromScan.objects.filter(pk=scan.id).update(reference=file, content=json.dumps(content))
        except Exception as e:
            messages.error(request, "Une erreur s'est produite durant la création.")
            return HttpResponseRedirect('/professor/lesson/'+str(pk)+'/test/from-scan/add/')

        for i in form:
            if not i[0] in "skills-scan" and not i[0] in "csrfmiddlewaretoken" and not i[0] in "titre":
                question = TestQuestionFromScan(question_num=int(i[0])+1, contexte=i[1], test_id=scan.id)
                try:
                    question.save()
                except Exception as e:
                    messages.error(request, "Une erreur s'est produite durant la création.")
                    return HttpResponseRedirect('/professor/lesson/'+str(pk)+'/test/from-scan/add/')


        return HttpResponseRedirect('/professor/lesson/'+str(pk)+'/test/')

    return render(request, "professor/lesson/test/from-scan/add.haml", {
        "lesson": lesson,
        "stages": lesson.stages_in_unchronological_order(),
    })

@user_is_professor
def lesson_test_from_scan_correct_one(request, lesson_pk, test_pk, pk):
    is_exist = TestAnswerFromScan.objects.filter(id__isnull=False).count()
    nb_not_match = TestAnswerFromScan.objects.filter(student_id__isnull=True).count()
    """if nb_not_match > 0 or is_exist == 0:
        messages.error(request,"Associez vos élèves avant de pouvoir corriger la réponse")
        return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/from-scan/' + str(test_pk) + '/')"""

    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=test_pk)
    answer = get_object_or_404(TestAnswerFromScan, pk=pk)
    questions = TestQuestionFromScan.objects.all().filter(test_id=test_pk).order_by('question_num')
    students = TestAnswerFromScan.objects.all().filter(test_id=test_pk).distinct('student_id').order_by('student_id','-is_correct')

    for st in students:
        an =  TestAnswerFromScan.objects.all().filter(test_id=test_pk,student_id = st.student_id, is_correct__isnull=False).count()
        st.pourcentage = str(an)+"/"+str(len(questions))


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
        "students":students,
        "match": nb_not_match,
    })

@user_is_professor
def lesson_test_from_scan_download(request, lesson_pk, pk):

    test = get_object_or_404(BaseTest, pk=pk)
    t = get_object_or_404(TestFromScan, pk=pk)

    if not t.reference is None:
        filename = settings.STATIC_ROOT+"/tests/pdf/"+str(pk)+".pdf" # Select your file here.
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='application/pdf')
        response['Content-Disposition'] = "filename="+test.name+".pdf"
        response['Content-Length'] = os.path.getsize(filename)
        return response
    else:
        return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/')

@user_is_professor
def lesson_test_from_scan_correct_by_student(request, lesson_pk, test_pk, pk):

    is_exist = TestAnswerFromScan.objects.filter(id__isnull=False, test_id=test_pk).count()
    nb_not_match = TestAnswerFromScan.objects.filter(student_id__isnull=True, test_id=test_pk).count()
    if nb_not_match > 0 or is_exist == 0:
        messages.error(request,"Associez vos élèves avant de pouvoir corriger la réponse")
        return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/from-scan/' + str(test_pk) + '/')

    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=test_pk)
    if (not 'sort_answer' in request.session) or (request.session['sort_answer'] is None or request.session['sort_answer'] == 0):
        request.session['sort_answer'] = 0;
        answers = TestAnswerFromScan.objects.all().filter(student_id=pk, test_id=test_pk).order_by('id')
    elif request.session['sort_answer'] == 1:
        answers = TestAnswerFromScan.objects.all().filter(student_id=pk,is_correct__isnull=True, test_id=test_pk).order_by('id')
    elif request.session['sort_answer'] == 2:
        answers = TestAnswerFromScan.objects.all().filter(student_id=pk, is_correct__isnull=False, test_id=test_pk).order_by('id')

    questions = TestQuestionFromScan.objects.all().filter(test_id=test_pk).order_by('question_num')
    students = TestAnswerFromScan.objects.all().filter(test_id=test_pk).distinct('student_id').order_by('student_id','-is_correct')

    for st in students:
        an =  TestAnswerFromScan.objects.all().filter(test_id=test_pk,student_id = st.student_id, is_correct__isnull=False).count()
        st.pourcentage = str(an)+"/"+str(len(questions))


    for answer in answers:
        if answer.annotation == None:
            answer.annotation = ""

    if request.method == "POST":

        if 'iscorrect' in request.POST:
            request.session['sort_answer'] = int(request.POST.get('iscorrect'))
            return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/from-scan/' + str(test_pk) + '/student/' + str(pk) + '/correct')
        else:
            form = request.POST.items()

            print(form)
            for tmp in form:
                print(tmp)

            t = {}
            c = {}
            for cor in form:
                if not cor[0] == "csrfmiddlewaretoken":
                    if 'c' in cor[0]:
                        c[int(cor[0][1:])] = cor[1]
                    elif 't' in cor[0]:
                        t[int(cor[0][1:])] = cor[1]

            for K,V in c.items():
                if K in t:
                    TestAnswerFromScan.objects.filter(pk=K).update(is_correct=V, annotation=t[K])
                else:
                    TestAnswerFromScan.objects.filter(pk=K).update(is_correct=V)

        return HttpResponseRedirect('/professor/lesson/' + str(lesson_pk) + '/test/from-scan/' + str(test_pk) + '/student/'+pk+'/correct')

    return render(request, "professor/lesson/test/from-scan/correct_by_student.haml", {
        "lesson": lesson,
        "test": test,
        "answers":answers,
        "questions":questions,
        "students":students,
        "stud":int(pk),
        "match":nb_not_match,
    })





@user_is_professor
def lesson_test_from_scan_detail(request, lesson_pk, pk):
    is_exist = TestAnswerFromScan.objects.filter(test_id=pk).count()
    nb_not_match = TestAnswerFromScan.objects.filter(student_id__isnull=True).count()

    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    test = get_object_or_404(TestFromScan, pk=pk)




    if (not 'sort_question' in request.session) or (request.session['sort_question'] is None or request.session['sort_question'] == -1):
        request.session['sort_question'] = -1;
        answers = TestAnswerFromScan.objects.all().filter(test_id=pk).order_by('id')
    else:
        answers = TestAnswerFromScan.objects.all().filter(test_id=pk, question_id=request.session['sort_question']).order_by('id')
    questions = TestQuestionFromScan.objects.all().filter(test_id=pk).order_by('question_num')
    students = TestAnswerFromScan.objects.all().filter(test_id=pk).distinct('student_id').order_by('student_id','-is_correct')


    for st in students:
        an =  TestAnswerFromScan.objects.all().filter(test_id=pk,student_id = st.student_id, is_correct__isnull=False).count()
        st.pourcentage = str(an)+"/"+str(len(questions))


    if request.method == "POST":
        if 'questions' in request.POST:
            request.session['sort_question'] = int(request.POST.get('questions'))
        elif 'copy' in request.FILES:

            form = ImportCopyForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():

                copy = request.FILES.getlist('copy', False)

                if not os.path.isdir(settings.STATIC_ROOT +"/tests/"+pk) and copy:
                    os.makedirs(settings.STATIC_ROOT +"/tests/"+pk)

                insertion_sort_file(copy)


                i=1
                count_question = 0
                cont = json.loads(test.content)
                count_page = 1
                count = 0
                format = ["png","PNG","jpg","jpeg","JPG","JPEG"]


                for c in copy:

                    split = str(c).split(".")

                    if split[1] in format:

                        img = Image.open(c)

                        dpi = int(round(img.size[0]/(21*0.3937008)))


                        if str(count_page) not in cont:
                            count_page = 1
                        numpage = str(count_page)

                        if count_page == 1:

                            ran = range(2,len(cont[numpage][0]),2)

                            x1 = pt_to_px(dpi,cont[numpage][0][0])
                            y1 = pt_to_px(dpi,cont[numpage][1][0],1)
                            x2 = pt_to_px(dpi,cont[numpage][0][1])
                            y2 = pt_to_px(dpi,cont[numpage][1][1],1)

                            name = img.crop((x1, y1, x2, y2))
                            ref_name = "/tests/"+ pk + "/name"+str(i)+".png"
                            name.save(settings.STATIC_ROOT +"/tests/"+ pk + "/name"+str(i)+".png")
                            count_question = 0
                        else:
                            ran = range(0,len(cont[numpage][0]),2)

                        for answ in ran:
                            answer = TestAnswerFromScan(test_id=pk, question_id=questions[count_question].id, reference_name=ref_name, reference='/tests/'+pk+'/crop'+str(i)+'.png')
                            answer.save()

                            x1 = pt_to_px(dpi,cont[numpage][0][answ])
                            y1 = pt_to_px(dpi,cont[numpage][1][answ],1)
                            x2 = pt_to_px(dpi,cont[numpage][0][answ+1])
                            y2 = pt_to_px(dpi,cont[numpage][1][answ+1],1)
                            img2 = img.crop((x1, y1, x2, y2))
                            img2.save(settings.STATIC_ROOT +"/tests/"+ pk + "/crop" + str(i) + ".png")
                            i += 1
                            count_question +=1
                    # It's a pdf
                    elif split[1] == "pdf":


                        # number of page per test
                        pages_per_test = PdfFileReader(settings.STATIC_ROOT +"/tests/pdf/"+pk+".pdf").getNumPages();

                        # Read the pdf file
                        reader = PdfFileReader(c, 'r')

                        default_storage.save(pk+".pdf", c)

                        all_pages = reader.getNumPages()

                        os.system("convert -density 150 %s %s"%(settings.MEDIA_ROOT+"/"+pk+".pdf",settings.STATIC_ROOT+"/tests/tmp/"+pk+".jpg"))

                        default_storage.delete(pk+".pdf")

                        for i in range(all_pages):

                            img = Image.open(settings.STATIC_ROOT+"/tests/tmp/"+pk+"-"+str(i)+".jpg")

                            dpi = int(round(img.size[0]/(21*0.3937008)))


                            if (i%pages_per_test) == 0:

                                ran = range(2,len(cont[str((i%pages_per_test)+1)][0]),2)

                                x1 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][0][0])
                                y1 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][1][0],1)
                                x2 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][0][1])
                                y2 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][1][1],1)

                                name = img.crop((x1, y1, x2, y2))
                                ref_name = "/tests/"+ pk + "/name"+str(count)+".png"
                                name.save(settings.STATIC_ROOT +"/tests/"+ pk + "/name"+str(count)+".png")
                                count_question = 0
                            else:
                                ran = range(0,len(cont[str((i%pages_per_test)+1)][0]),2)

                            for answ in ran:

                                answer = TestAnswerFromScan(test_id=pk, question_id=questions[count_question].id, reference_name=ref_name, reference='/tests/'+pk+'/crop'+str(count)+'.png')
                                answer.save()

                                x1 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][0][answ])
                                y1 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][1][answ],1)
                                x2 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][0][answ+1])
                                y2 = pt_to_px(dpi,cont[str((i%pages_per_test)+1)][1][answ+1],1)
                                img2 = img.crop((x1, y1, x2, y2))
                                img2.save(settings.STATIC_ROOT +"/tests/"+ pk + "/crop" + str(count) + ".png")
                                count_question +=1
                                count+=1





                    else:
                        messages.error(request,"Le format ne correspond pas à la norme")
                        return HttpResponseRedirect('/professor/lesson/'+str(lesson_pk)+'/test/from-scan/'+str(pk)+'/')

                    count_page+=1
        return HttpResponseRedirect('/professor/lesson/'+str(lesson_pk)+'/test/from-scan/'+str(pk)+'/')

    return render(request, "professor/lesson/test/from-scan/detail.haml", {
        "lesson": lesson,
        "test":test,
        "answers":answers,
        "questions": questions,
        "students": students,
        "match": nb_not_match,
        "exist": is_exist

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
