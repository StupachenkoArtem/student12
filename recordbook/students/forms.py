from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from students.models import Group, Student, Subject, Gradebook


# class AddStudentForm(forms.Form):
#     first_name = forms.CharField(label='Имя', max_length=50)
#     last_name = forms.CharField(label='Фамилия', max_length=50)
#     middle_name = forms.CharField(label='Отчество', max_length=50)
#     email = forms.EmailField(label='e-mail')
#     birth_date = forms.DateField(label='Дата Рождения')
#     is_study = forms.BooleanField(label='Учится', required=False, initial=True)
#     group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), empty_label='Не выбрана')
#     slug = forms.SlugField(label='URL', max_length=255)


class AddStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = 'Не выбрана'

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'birth_date', 'is_study', 'group', 'photo',
                  'group', 'slug']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError('Недопустимые символы')
        return first_name


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FilterStudentForm(forms.Form):
    last_name = forms.CharField(label='Фамилия', max_length=50, required=False)
    first_name = forms.CharField(label='Имя', max_length=50, required=False)
    group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), empty_label='', required=False)


class YourModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class ChooseGroupForm(forms.Form):
    group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), empty_label='Не выбрана', required=False)


class ChooseSubjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group', None)
        super(ChooseSubjectForm, self).__init__(*args, **kwargs)
        if self.group:
            group = Group.objects.filter(id=self.group)[0]
            self.fields['subject'].queryset = group.subject_set.all()

    subject = forms.ModelChoiceField(label='Предмет', queryset=Subject.objects.none(), empty_label='Не выбран', required=False)


class AddMarkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student = args[0]['student'] if args else None
        if student:
            student = Student.objects.filter(id=student)[0]
            self.fields['student'].queryset = Student.objects.filter(group=student.group)

    class Meta:
        model = Gradebook
        fields = ['subject', 'student', 'date', 'mark']
