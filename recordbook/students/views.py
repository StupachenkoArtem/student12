from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, \
    CreateView, DeleteView, UpdateView
from .filters import StudentFilter
from .models import Student
from .forms import AddStudentForm, LoginUserForm, ChooseGroupForm, \
    ChooseSubjectForm, AddMarkForm
from .utils import menu, DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class StudentHome(DataMixin, ListView):
    model = Student
    template_name = 'students/index.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        st_filter = StudentFilter(self.request.GET, queryset)
        return st_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        queryset = self.get_queryset()
        st_filter = StudentFilter(self.request.GET, queryset)
        c_def = self.get_user_context(title='Главная страница', auth=auth,
                                      st_filter=st_filter)
        return {**context, **c_def}


def groups(request, group):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Здесь выводятся группы.</h1><h2>{group}</h2>")


def about(request):
    return render(request, 'students/about.html',
                  {'menu': menu, 'title': 'О сайте'})


def students(request):
    return HttpResponse("Студенты")


def teachers(request):
    return HttpResponse("Преподователи")


class ShowStudent(DataMixin, DetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        c_def = \
            self.get_user_context(title=kwargs['object'].last_name, auth=auth)
        print(kwargs['object'].last_name)
        return {**context, **c_def}

    model = Student
    template_name = 'students/student.html'
    slug_url_kwarg = 'stud_slug'
    context_object_name = 'st'


class AddStudent(LoginRequiredMixin, CreateView):
    form_class = AddStudentForm
    template_name = 'students/addstudent.html'
    login_url = reverse_lazy('home')
    raise_exception = True

    def form_valid(self, form):
        student = form.save(commit=False)
        student.user = User.objects.get(username=self.request.user)
        student.save()
        return redirect(reverse('home'))


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return {**context, **c_def}


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'students/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class DeleteStudent(LoginRequiredMixin, DataMixin, DeleteView):
    model = Student
    template_name = 'students/delete_student.html'
    success_url = reverse_lazy('home')
    context_object_name = 'st'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удалить студента')
        return {**context, **c_def}


class UpdateStudent(LoginRequiredMixin, DataMixin, UpdateView):
    model = Student
    form_class = AddStudentForm
    template_name = 'students/update_student.html'
    success_url = reverse_lazy('home')
    context_object_name = 'st'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменить студента')
        return {**context, **c_def}


class Gradebook(DataMixin, ListView):
    template_name = 'students/gradebook.html'
    context_object_name = 'students'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        group = self.request.GET.get('group')
        subject = self.request.GET.get('subject')
        dates = set()
        studs = []
        if group and subject:
            selected_students = Student.objects.filter(group=group)
            for st in selected_students:
                for sub in st.gradebook_set.filter(subject=subject):
                    dates.add(sub.date)
            dates = sorted(dates)
            for st in selected_students:
                marks = [''] * len(dates)
                for sub in st.gradebook_set.filter(subject=subject):
                    marks[dates.index(sub.date)] = sub.mark
                studs.append((st.pk, f'{st.last_name}'
                                     f' {st.first_name[0]}.'
                                     f'{st.middle_name[0]}.', marks))
        c_def = self.get_user_context(title='Журнал успеваемости',
                                      auth=auth,
                                      group_form=ChooseGroupForm(self.request.
                                                                 GET),
                                      subj_form=ChooseSubjectForm
                                      (self.request.GET, group=group),
                                      group=group,
                                      subject=subject,
                                      dates=dates,
                                      studs=studs)
        return {**context, **c_def}

    def get_queryset(self):
        group = self.request.GET.get('group')
        group = 0 if group == '' else group
        return Student.objects.filter(group=group)


class AddMark(DataMixin, CreateView):
    form_class = AddMarkForm
    template_name = 'students/add_mark.html'
    success_url = reverse_lazy('gradebook')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить оценку",
                                      form=AddMarkForm(self.request.GET))
        return {**context, **c_def}
