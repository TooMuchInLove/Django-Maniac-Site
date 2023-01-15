from .models import Project
from django.db.models import Q
from django.shortcuts import redirect


def project_author(func):
    def wrapper(request, pk):
        obj = Project.objects.get(id=pk)
        if request.user == getattr(obj, 'author'):
            return func(request, pk)
        else:
            return redirect('profile')
    return wrapper


def project_member(func):  #Функция вешается поверх функции отрисовки формы
    def wrapper(request, id_project):
        project = Project.objects.get(id=id_project)
        project_members = Project.objects.filter(Q(author=request.user) | Q(members=request.user))
        if project in project_members:
            return func(request, id_project)
        else:
            return redirect('profile')
    return wrapper


def is_member_posting(func):  # Для представления редактирования статьи, чекнуть безопасность
    def wrapper(request, id_project, id_article):
        project = Project.objects.get(id=id_project)
        project_members = Project.objects.filter(Q(author=request.user) | Q(members=request.user))
        if project in project_members:
            return func(request, id_project, id_article)
        else:
            return redirect('profile')
    return wrapper
