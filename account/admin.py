from django.contrib import admin
from .models import UserProfile, Project, SubscriptionRelation, ProjectMessage

admin.site.register([UserProfile, Project, SubscriptionRelation, ProjectMessage])
