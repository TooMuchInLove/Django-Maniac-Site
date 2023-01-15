from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Project, UserProfile
from OnlineMedia.models import Article


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'email')
#
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Никнейм (уникальный)')
    first_name = forms.CharField(label='Имя, фамилия')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def save(self, commit=True):
        # user = super(self, UserRegistrationForm).save(commit=False) # раньше работало
        user = UserCreationForm.save(self, commit=False)  # теперь работает так
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class ProjectRegisterForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', )
        labels = {'name': 'Название'}


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=250, required=True, label='', widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Имя, фамилия'}))
    email = forms.EmailField(max_length=250, required=True, label='', widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'email')


class EditProfileForm(forms.ModelForm):
    description = forms.CharField(max_length=250, required=False, label='', widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Описание'}))
    image = forms.ImageField(label='Фотография', required=False)

    class Meta:
        model = UserProfile
        fields = ['description', 'image']


class EditProject(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label='', widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'Название'}))
    description = forms.CharField(max_length=250, label='', widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'Описание'}))
    city = forms.CharField(max_length=250, required=False, label='', widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'Город'}))
    image = forms.ImageField(required=False, label='Логотип')

    class Meta:
        model = Project
        fields = ['name', 'description', 'city', 'image']


class UserChoice(forms.Form):
    username = forms.CharField(max_length=50, required=True, label='', widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'никнейм'}))


class CreateArticle(forms.ModelForm):
    title = forms.CharField(max_length=250, label='', widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'Заголовок'}))
    preview_text = forms.CharField(max_length=250, label='', widget=forms.TextInput(
         attrs={'class': 'form-control', 'placeholder': 'Краткое описание'}))
    preview_img = forms.ImageField(label="Изображение")
    text = forms.CharField(max_length=50, required=True, label='', widget=forms.Textarea(
                                  attrs={'class': 'form-control', 'placeholder': 'Текст статьи'}))

    class Meta:
        model = Article
        fields = ('title', 'preview_text', 'text', 'preview_img', 'id_section', 'tag')
