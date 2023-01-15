from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_author')
    members = models.ManyToManyField(User, related_name='project_members', blank=True)
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='projects_image', blank=True)

    def __str__(self):
        return str(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='profiles_image', blank=True)
    # subscription_user = models.ManyToManyField(User, related_name='user', blank=True)
    # subscription_project = models.ManyToManyField(Project, related_name='project', blank=True)
    user_followed = models.ManyToManyField('self', related_name='user_following', symmetrical=False, through='SubscriptionRelation')
    project_followed = models.ManyToManyField(Project, related_name='project_following', blank=True)

    def __str__(self):
        return str(self.user) + ' profile'

    @receiver(post_save, sender=User)
    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])


class SubscriptionRelation(models.Model):
    user_from = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_to')

    def __str__(self):
        return str(self.user_from.user) + ' - ' + str(self.user_to.user)


class ProjectMessage(models.Model):
    sender = models.ForeignKey(Project, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,)
    confirm = models.BooleanField()


# class Subscription(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     subscription_user = models.ManyToManyField(User, related_name='user', blank=True)
#     subscription_project = models.ManyToManyField(Project, related_name='project', blank=True)
#
#     def __str__(self):
#         return str(self.user) + ' subscriptions'
#
#     @receiver(post_save, sender=User)
#     def create_profile(sender, **kwargs):
#         if kwargs['created']:
#             user_profile = UserProfile.objects.create(user=kwargs['instance'])





