from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm, AcademicGroupForm, CourseForm
from .models import Department, AcademicGroup, Course, StudentProfile


def is_methodist(user):
    return user.groups.filter(name='Методист').exists()


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'is_methodist': is_methodist(request.user)
    })


@login_required
def dashboard(request):
    departments = Department.objects.all()
    groups = AcademicGroup.objects.all()
    courses = Course.objects.all()

    popular_courses = sorted(
        [(item.title, item.students.count()) for item in courses],
        key=lambda item: item[1],
        reverse=True
    )[:8]

    return render(request, 'dashboard.html', {
        'department_names': [item.name for item in departments],
        'groups_count': [item.groups.count() for item in departments],
        'courses_count': [item.courses.count() for item in departments],
        'students_count': [item.students.count() for item in departments],

        'group_names': [item.name for item in groups],
        'group_students_count': [item.students.count() for item in groups],

        'course_names': [item[0] for item in popular_courses],
        'course_students_count': [item[1] for item in popular_courses],

        'total_departments': Department.objects.count(),
        'total_groups': AcademicGroup.objects.count(),
        'total_courses': Course.objects.count(),
        'total_students': StudentProfile.objects.count(),
    })


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {
        'departments': departments,
        'is_methodist': is_methodist(request.user),
    })


@login_required
@user_passes_test(is_methodist)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()

    return render(request, 'object_form.html', {
        'form': form,
        'title': 'Добавление факультета'
    })


@login_required
@user_passes_test(is_methodist)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'object_form.html', {
        'form': form,
        'title': 'Изменение факультета'
    })


@login_required
@user_passes_test(is_methodist)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        department.delete()
        return redirect('department_list')

    return render(request, 'object_confirm_delete.html', {
        'object': department,
        'title': 'Удаление факультета'
    })


@login_required
def academic_group_list(request):
    academic_groups = AcademicGroup.objects.all()
    return render(request, 'academic_group_list.html', {
        'academic_groups': academic_groups,
        'is_methodist': is_methodist(request.user),
    })


@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm()

    return render(request, 'object_form.html', {
        'form': form,
        'title': 'Добавление группы'
    })


@login_required
@user_passes_test(is_methodist)
def academic_group_update(request, id):
    academic_group = get_object_or_404(AcademicGroup, id=id)

    if request.method == 'POST':
        form = AcademicGroupForm(request.POST, instance=academic_group)
        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm(instance=academic_group)

    return render(request, 'object_form.html', {
        'form': form,
        'title': 'Изменение группы'
    })


@login_required
@user_passes_test(is_methodist)
def academic_group_delete(request, id):
    academic_group = get_object_or_404(AcademicGroup, id=id)

    if request.method == 'POST':
        academic_group.delete()
        return redirect('academic_group_list')

    return render(request, 'object_confirm_delete.html', {
        'object': academic_group,
        'title': 'Удаление группы'
    })


@login_required
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {
        'courses': courses,
        'is_methodist': is_methodist(request.user),
    })


@login_required
@user_passes_test(is_methodist)
def courses_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm()

    return render(request, 'object_form.html', {
        'form': form,
        'title': 'Добавление курса'
    })


@login_required
@user_passes_test(is_methodist)
def courses_update(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'object_form.html', {
        'form': form,
        'title': 'Изменение курса'
    })


@login_required
@user_passes_test(is_methodist)
def courses_delete(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        course.delete()
        return redirect('courses_list')

    return render(request, 'object_confirm_delete.html', {
        'object': course,
        'title': 'Удаление курса'
    })
