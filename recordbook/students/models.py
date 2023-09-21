from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Group(models.Model):
    name = models.CharField(verbose_name='Группа', max_length=5)
    course = models.CharField(verbose_name='Курс', max_length=2)
    enrollment_year = models.IntegerField(verbose_name='Год зачисления')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['course', 'enrollment_year']

    def __str__(self):
        return f'{self.course}-{self.name}'


class Student(models.Model):
    objects = models.Model
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    middle_name = models.CharField(verbose_name='Отчество', max_length=50)
    email = models.EmailField(verbose_name='e-mail', blank=True)
    birth_date = models.DateField(verbose_name='Дата Рождения', default=date(1975, 9, 5))
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    is_study = models.BooleanField(verbose_name='Учится', default=True)
    photo = models.ImageField(verbose_name='Фото', upload_to="photos/%Y/%m/%d")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name='Группа')
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('student', kwargs={'stud_slug': self.slug})


class Teacher(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    middle_name = models.CharField(verbose_name='Отчество', max_length=50)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDERS)
    email = models.EmailField(verbose_name='e-mail', blank=True)
    birth_date = models.DateField(verbose_name='Дата Рождения', default=date(1975, 9, 5))
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    photo = models.ImageField(verbose_name='Фото', upload_to="photos/%Y/%m/%d")
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def fio(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Преподователь'
        verbose_name_plural = 'Преподователи'
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Subject(models.Model):
    name = models.CharField(verbose_name='Предмет', max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподователь', related_name='get_subjects')
    groups = models.ManyToManyField(Group, verbose_name='Группы')
    students = models.ManyToManyField(Student, through='Gradebook', verbose_name='Студенты')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class Gradebook(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    date = models.DateField(verbose_name='Дата')
    mark = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.subject}-{self.student}'