from django.http import HttpResponseRedirect
from .forms import LoginForm, UserRegistrationForm, ProjectRegisterForm, EditProfileForm, EditUserForm, EditProject, UserChoice, CreateArticle
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Project, SubscriptionRelation, ProjectMessage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from .my_decorators import project_author
from django.core.exceptions import ObjectDoesNotExist
from OnlineMedia.models import Article

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'registration/login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(user_form.cleaned_data['password'])
#             new_user.save()
#             return render(request, 'account/register_done.html', {'new_user': new_user})
#         else:
#             return render(request, 'account/register.html', {'user_form': user_form})
#     else:
#         user_form = UserRegistrationForm()
#         return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'account/register.html', {'user_form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': form})


@login_required
def profile_view(request):
    return redirect(reverse('profile_projects', kwargs={'pk': request.user.id}))


@login_required
def profile_view_pk(request, pk=None):
    return redirect(reverse('profile_projects', kwargs={'pk': pk}))


def get_user_and_project(pk=None):
    user = get_object_or_404(User, id=pk)
    projects = Project.objects.filter(Q(author=user) | Q(members=user))
    message_count = user.projectmessage_set.filter(confirm=False).count
    return {'user1': user, 'projects': projects, 'message_count': message_count}


def profile_blog_view(request, pk=None):
    user_and_projects = get_user_and_project(pk)
    dict = {'blog': 'True'}
    dict.update(user_and_projects)
    return render(request, 'profile/user_projects.html', dict)


def profile_projects(request, pk=None):
    user_and_projects = get_user_and_project(pk)
    dict = {'userprojects': 'True'}
    dict.update(user_and_projects)
    return render(request, 'profile/user_projects.html', dict)


def register_project(request):
    if request.method == 'POST':
        project_form = ProjectRegisterForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('/account/profile/1/projects')  # На этой строчке был Лексов.
        else:
            return render(request, 'project/register_project.html', {'project_form': project_form})
    else:
        project_form = ProjectRegisterForm()
        return render(request, 'project/register_project.html', {'project_form': project_form})


def users_list(request):                  # сделал для вывода всех пользователей, на сайте не должно быть, т.е. удалить
    users = User.objects.all()
    projects = Project.objects.all()
    subs = request.user.userprofile.user_followed.all()
    subs2 = request.user.userprofile.user_following.all()
    subs_project = request.user.userprofile.project_followed.all()
    return render(request, 'users_list.html', {'users': users, 'projects': projects, 'subs': subs, 'subs2': subs2, 'subs_project': subs_project})


@login_required()
def profile_edit(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES,  instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # return redirect('profile')
        # else:
              # return render(request, 'profile/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.userprofile)
    dict = {'user1': request.user, 'user_form': user_form, 'profile_form': profile_form,  'settings': 'true', }
    user_and_projects = get_user_and_project(request.user.id)
    dict.update(user_and_projects)
    return render(request, 'profile/profile_edit.html', dict)


@login_required()
def password_edit(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user=request.user)
    dict = {'password_form': password_form, 'password': 'true'}
    user_and_projects = get_user_and_project(request.user.id)
    dict.update(user_and_projects)
    return render(request, 'profile/password_edit.html', dict)


def profile_notifications(request):
    invitations = ProjectMessage.objects.filter(receiver=request.user, confirm=False)
    dict = {'invitations': invitations, 'notifications': 'true',}
    user_and_projects = get_user_and_project(request.user.id)
    dict.update(user_and_projects)
    return render(request, 'profile/profile_notifications.html', dict)


def profile_subscriptions(request, pk=None):
    user1 = get_object_or_404(User, id=pk)
    userprofile_followed = user1.userprofile.user_followed.all()
    project_followed = user1.userprofile.project_followed.all()
    message_count = request.user.projectmessage_set.filter(confirm=False).count
    return render(request, 'profile/profile_subscriptions.html', {'user1': user1, 'userprofile_followed': userprofile_followed,
                                                                  'project_followed': project_followed, 'message_count': message_count} )


def answer_to_invite(request, operation=None, pk=None):
    # project = Project.objects.get(id=pk)
    if operation == 'accept':
        # invite = ProjectMessage.objects.get(sender=project, receiver=request.user, confirm=False)
        invite = ProjectMessage.objects.get(id=pk, confirm=False)
        invite.confirm = True
        invite.save()
        project = Project.objects.get(id=ProjectMessage.objects.get(id=pk).sender.id)
        project.members.add(request.user)
    elif operation == 'refuse':
        # invite = ProjectMessage.objects.get(sender=project, receiver=request.user, confirm=False)
        invite = ProjectMessage.objects.get(id=pk, confirm=False)
        invite.delete()
    return redirect('profile_notifications')


def get_info_project(pk=None):
    project = get_object_or_404(Project, id=pk)
    members = User.objects.filter(project_members=project)
    author = get_object_or_404(User, project_author=project)
    return {'project': project, 'members': members, 'author': author}


def project_blog(request, pk=None):
    # dict = {'blog': 'True'}
    # info_project = get_info_project(pk)
    # dict.update(info_project)
    project = Project.objects.get(id=pk)
    if project in Project.objects.filter(Q(author=request.user) | Q(members=request.user)):
        showArticle = True
    else: 
        showArticle = False
    message = ''
    if request.method == 'POST':
        form = CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.id_project = project
            article.save()
            message = 'Статья опубликована!'
    else:
        form = CreateArticle()
    articles = Article.objects.filter(id_project=project)
    author = get_object_or_404(User, project_author=project)
    return render(request, 'project/project_blog.html', {'project': project, 'articles':articles, 'author': author,
                                                         'blog': 'True', 'form': form, 'message': message,
                                                         'showArticle': showArticle})


def project_members(request, pk=None):
    dict = {'project_members': 'True'}
    info_project = get_info_project(pk)
    dict.update(info_project)
    return render(request, 'project/project_members.html', dict)


@project_author
def project_edit(request, pk=None):
    if request.method == 'POST':
        # form_user_choice = UserChoice(request.POST)
        project_form = EditProject(request.POST, request.FILES, instance=Project.objects.get(id=pk))
        if project_form.is_valid():
            project_form.save()
    else:
        project_form = EditProject(instance=Project.objects.get(id=pk))
    dict = {'project_form': project_form, 'settings': 'true',}
    info_project = get_info_project(pk)
    dict.update(info_project)
    return render(request, 'project/project_edit.html', dict)


@project_author
def add_member(request, pk=None):
    if request.method == 'POST':
        form_user_choice = UserChoice(request.POST)
        if form_user_choice.is_valid():
            username = form_user_choice.cleaned_data['username']
            try:
                receiver = User.objects.get(username=username)
                if receiver not in Project.objects.get(id=pk).members.all():
                    # if ProjectMessage.objects.filter()
                    obj, created = ProjectMessage.objects.get_or_create(sender=Project.objects.get(id=pk), receiver=receiver, confirm=False)
                    if created:
                        message = "Приглашение отправлено"
                    else:
                        message = "Вы уже отправили приглашение этому пользователю"
                else:
                    message = "Пользователь уже в вашей команде"
            except ObjectDoesNotExist:
                message = "Пользователей с таким никнеймом нет"
        else:
            message = "Вы неправильно заполнили форму"
    else:
        form_user_choice = UserChoice()
        message = ''
    dict = {'form_user_choice': form_user_choice, 'message': message}
    info_project = get_info_project(pk)
    dict.update(info_project)
    return render(request, 'project/add_member.html', dict)


def project_followers(request, pk=None):
    followers = Project.objects.get(id=pk).project_following.all()
    dict = {'followers': followers, 'subscriptions': 'true'}
    info_project = get_info_project(pk)
    dict.update(info_project)
    return render(request, 'project/project_followers.html', dict)


@login_required()
def change_subscription(request, model, operation, pk):
    user_from = request.user.userprofile
    if model == 'User':
        user_to = User.objects.get(id=pk).userprofile
        if operation == 'add':
           relation = SubscriptionRelation.objects.create(user_from=user_from, user_to=user_to)
        elif operation == 'remove':
           relation = SubscriptionRelation.objects.filter(user_from=user_from, user_to=user_to).delete()
        return redirect('profile')
    elif model == 'Project':
        if operation == 'add':
            user_from.project_followed.add(Project.objects.get(id=pk))
        elif operation == 'remove':
            user_from.project_followed.remove(Project.objects.get(id=pk))
        return redirect('profile')










