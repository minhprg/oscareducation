import json

from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Count

from skills.models import Skill, StudentSkill
from examinations.models import Test, TestStudent, Exercice

from .models import Lesson, Student
from .forms import LessonForm, StudentForm, VideoSkillForm, ExternalLinkSkillForm, ExerciceSkillForm, SyntheseForm
from .utils import generate_random_password, user_is_professor


@user_is_professor
def dashboard(request):
    form = LessonForm(request.POST) if request.method == "POST" else LessonForm()

    if form.is_valid():
        lesson = form.save()
        lesson.professors.add(request.user.professor)
        return HttpResponseRedirect(reverse("professor_dashboard"))

    return render(request, "professor/dashboard.haml", {
        "lessons": Lesson.objects.filter(professors=request.user.professor).annotate(Count("students")),
        "add_lesson_form": form,
    })


@user_is_professor
def lesson_detail_view(request, pk):
    form = StudentForm(request.POST) if request.method == "POST" else StudentForm()

    lesson = get_object_or_404(Lesson, pk=pk)

    # TODO: a professor can only see one of his lesson

    if form.is_valid():
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        username = form.generate_student_username()
        email = form.generate_email(username)

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=generate_random_password(15),
                                        first_name=first_name,
                                        last_name=last_name)

        student = Student.objects.create(user=user)
        student.lesson_set.add(lesson)
        # TODO send email to student here if email doesn't end in @example.com

        skills_to_handle = list(lesson.stage.skill_set.all())
        handled_skills = []
        with transaction.atomic():
            while skills_to_handle:
                skill = skills_to_handle.pop()

                StudentSkill.objects.create(
                    student=student,
                    skill=skill,
                )

                handled_skills.append(skill)
                skills_to_handle.extend(list(filter(lambda x: x not in handled_skills, skill.depends_on.all())))

        return HttpResponseRedirect(reverse("professor_lesson_detail_view", args=(lesson.pk,)))

    return render(request, "professor/lesson_detail_view.haml", {
        "lesson": lesson,
        "add_student_form": form,
    })


@user_is_professor
def student_detail_view(request, pk):
    # TODO: a professor can only see one of his students

    student = get_object_or_404(Student, pk=pk)

    return render(request, "professor/student_detail_view.haml", {
        "student": student,
    })


@require_POST
@user_is_professor
def regenerate_student_password(request):
    data = json.load(request)

    student = get_object_or_404(Student, id=data["student_id"])
    new_password = student.generate_new_password()

    # TODO: a professor can only modify this for one of his students

    return HttpResponse(new_password)


@require_POST
@user_is_professor
def validate_student_skill(request, student_skill):
    # TODO: a professor can only do this on one of his students

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.validate()

    return HttpResponseRedirect(reverse('professor_student_detail_view', args=(student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def unvalidate_student_skill(request, student_skill):
    # TODO: a professor can only do this on one of his students

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.unvalidate()

    return HttpResponseRedirect(reverse('professor_student_detail_view', args=(student_skill.student.id,)) + "#skills")


@require_POST
@user_is_professor
def default_student_skill(request, student_skill):
    # TODO: a professor can only do this on one of his students

    student_skill = get_object_or_404(StudentSkill, id=student_skill)

    student_skill.default()

    return HttpResponseRedirect(reverse('professor_student_detail_view', args=(student_skill.student.id,)) + "#skills")


@user_is_professor
def lesson_tests_and_skills(request, lesson_id):
    # TODO: a professor can only see one of his lesson

    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    return HttpResponse(json.dumps({
        "tests": [{"name": x.name, "skills": list(x.skills.all().values("code")), "type": x.display_test_type(), "id": x.id} for x in lesson.test_set.all()],
        "skills": [x for x in Skill.objects.values("id", "code", "name").order_by('-code')],
    }, indent=4))


@require_POST
@user_is_professor
def add_test_for_lesson(request):
    # TODO: a professor can only do this on one of his lesson

    data = json.load(request)

    lesson = get_object_or_404(Lesson, id=data["lesson"])

    if request.user.professor not in lesson.professors.all():
        raise PermissionDenied()

    with transaction.atomic():
        test = Test.objects.create(
            lesson=lesson,
            name=data["name"],
            type=data["type"],
        )

        for skill_id in data["skills"]:
            test.skills.add(Skill.objects.get(code=skill_id))

        for student in lesson.students.all():
            TestStudent.objects.create(
                test=test,
                student=student,
            )

        if data["type"] == "skills":
            test.generate_skills_test()
        elif data["type"] == "dependencies":
            test.generate_dependencies_test()
        elif data["type"] == "skills-dependencies":
            test.generate_skills_dependencies_test()
        else:
            raise Exception()

        test.save()

    return HttpResponse("ok")


@user_is_professor
def exercice_list(request):
    return render(request, 'professor/exercice_list.haml', {
        "exercice_list": Exercice.objects.select_related('skill'),
        "skills_without_exercices": Skill.objects.filter(exercice__isnull=True),
    })


@require_POST
@user_is_professor
def students_password_page(request, pk):
    # TODO: a professor can only do this on one of his student
    lesson = get_object_or_404(Lesson, pk=pk)

    students = []

    with transaction.atomic():
        for student in lesson.students.all():
            students.append({
                "last_name": student.user.last_name,
                "first_name": student.user.first_name,
                "username": student.user.username,
                "password": student.generate_new_password(),
            })

    return render(request, "professor/students_password_page.haml", {
        "students": students
    })


@user_is_professor
def edit_pedagogical_ressources(request, slug):
    skill = get_object_or_404(Skill, code=slug)

    if request.method == "GET":
        return render(request, "professor/skills_edit_professor.haml", {
            "video_skill_form": VideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })

    assert request.method == "POST"

    print request.POST

    if request.POST["form_type"] == "video_skill":
        form = VideoSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor_skill_edit_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skills_edit_professor.haml", {
            "video_skill_form": form,
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })

    elif request.POST["form_type"] == "exercice_skill":
        form = ExerciceSkillForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor_skill_edit_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skills_edit_professor.haml", {
            "video_skill_form": VideoSkillForm(),
            "exercice_skill_form": form,
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": SyntheseForm(),
            "object": skill,
        })
    elif request.POST["form_type"] == "external_link_skill":
        form = ExternalLinkSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor_skill_edit_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skills_edit_professor.haml", {
            "video_skill_form": VideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": form,
            "synthese_form": SyntheseForm(),
            "object": skill,
        })
    elif request.POST["form_type"] == "synthese_form":
        form = SyntheseForm(request.POST)
        if form.is_valid():
            skill.oscar_synthese = form.cleaned_data["synthese"]
            skill.save()
            return HttpResponseRedirect(reverse('professor_skill_edit_pedagogical_ressources', args=(skill.code,)))

        return render(request, "professor/skills_edit_professor.haml", {
            "video_skill_form": VideoSkillForm(),
            "exercice_skill_form": ExerciceSkillForm(),
            "external_link_skill_form": ExternalLinkSkillForm(),
            "synthese_form": form,
            "object": skill,
        })
