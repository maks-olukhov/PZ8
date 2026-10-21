import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model  # Используем фабрику для получения модели пользователя
from accounts.models import Department, AcademicGroup, Course, StudentProfile
from tickets.models import Category 

def create_demo_data():
    User = get_user_model()
    department_names = [
        'Информационные технологии',
        'Прикладная физика',
        'Экономика',
        'Дизайн',
        'Прикладная математика',
    ]


    departments = {}
    for name in department_names:
        department, _ = Department.objects.get_or_create(name=name)
        departments[name] = department

    group_data = {
        'Информационные технологии': ['ИТ-101', 'ИТ-201'],
        'Прикладная физика': ['ФИЗ-101', 'ФИЗ-201'],
        'Экономика': ['ЭК-101', 'ЭК-201'],
        'Дизайн': ['ДИЗ-101'],
        'Прикладная математика': ['ПМ-101', 'ПМ-201'],
    }

    groups = {}
    for department_name, names in group_data.items():
        for name in names:
            group, _ = AcademicGroup.objects.get_or_create(
                name=name,
                department=departments[department_name]
            )
            groups[name] = group

    course_data = {
        'Информационные технологии': [
            'Веб-программирование', 'Базы данных', 'Python', 'Алгоритмы'
        ],
        'Прикладная физика': [
            'Общая физика', 'Механика', 'Электроника'
        ],
        'Экономика': [
            'Микроэкономика', 'Макроэкономика', 'Эконометрика', 'Финансы'
        ],
        'Дизайн': [
            'Основы дизайна', 'UX/UI', 'Компьютерная графика'
        ],
        'Прикладная математика': [
            'Математический анализ', 'Линейная алгебра',
            'Теория вероятностей', 'Численные методы'
        ],
    }

    courses = {}
    for department_name, titles in course_data.items():
        for title in titles:
            course, _ = Course.objects.get_or_create(
                title=title,
                department=departments[department_name],
                defaults={'description': 'Учебный курс'}
            )
            courses.setdefault(department_name, []).append(course)

    students_by_group = {
        'ИТ-101': 4,
        'ИТ-201': 4,
        'ФИЗ-101': 3,
        'ФИЗ-201': 2,
        'ЭК-101': 4,
        'ЭК-201': 3,
        'ДИЗ-101': 4,
        'ПМ-101': 4,
        'ПМ-201': 3,
    }

    student1 = User.objects.filter(username='student1').first()
    if student1:
        profile, _ = StudentProfile.objects.get_or_create(user=student1)
        profile.department = departments['Информационные технологии']
        profile.academic_group = groups['ИТ-101']
        profile.save()
        profile.courses.set(courses['Информационные технологии'][:3])

    number = 1
    for group_name, count in students_by_group.items():
        group = groups[group_name]
        department = group.department

        for i in range(count):
            username = f'demo_student_{number:02d}'
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.first_name = 'Студент'
                user.last_name = str(number)
                user.save()

            profile, _ = StudentProfile.objects.get_or_create(user=user)
            profile.department = department
            profile.academic_group = group
            profile.save()

            department_courses = courses[department.name]
            profile.courses.clear()
            profile.courses.add(department_courses[0])
            profile.courses.add(department_courses[(i + 1) % len(department_courses)])
            if i % 2 == 0 and len(department_courses) > 2:
                profile.courses.add(department_courses[2])

            number += 1

    print('Демонстрационные данные добавлены.')


def create_admin_if_not_exists():
    User = get_user_model()
    username = os.getenv('ADMIN_USERNAME', 'admin')
    password = os.getenv('ADMIN_PASSWORD')
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    
    if password and not User.objects.filter(username=username).exists():
        print(f"Административная процедура: создание суперпользователя {username}...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Суперпользователь успешно создан.")
    elif not password:
        print("Внимание: Переменная ADMIN_PASSWORD не задана. Суперпользователь не создан.")
def create_ticket_categories():
    """Безопасная административная процедура создания категорий тикетов"""
    categories_list = [
        'Техническая поддержка',
        'Пароли',
        'Академические вопросы',
        'Оплата обучения',
        'Администрация',
    ]
    
    print("Административная процедура: создание категорий тикетов...")
    for cat_name in categories_list:
        # Метод get_or_create гарантирует, что дубликаты не создадутся при повторном деплое
        category, created = Category.objects.get_or_create(name=cat_name)
        if created:
            print(f"Категория '{cat_name}' успешно создана.")
    print("Проверка категорий завершена.")


if __name__ == '__main__':
    create_demo_data()
    create_admin_if_not_exists()
    create_ticket_categories()
