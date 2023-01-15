from django.contrib import admin
from .models import Genres, Artists, Cities, Relase, Group_Members, Management, Gallery, Videos, Poster

admin.site.register(Genres)
admin.site.register(Cities)


class RelaseInLine(admin.TabularInline):
    model = Relase


class Group_MembersInLine(admin.TabularInline):
    model = Group_Members


class ManagementInLine(admin.TabularInline):
    model = Management


class GalleryInLine(admin.TabularInline):
    model = Gallery


class VideosInLine(admin.TabularInline):
    model = Videos


class PostersInLine(admin.TabularInline):
    model = Poster


@admin.register(Artists)
class ArtistsAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_of_found', 'main_genre', 'city', 'LPRname', 'feedback')
    fieldsets = (
        ('Контакты артиста', {
            'fields': (('name', 'year_of_found', 'city', 'image'), 'main_genre', 'genre', 'vklink', 'websitelink', 'text', 'feedback')
        }),
        ('Контакты ЛПР', {
            'fields': ('LPRname', 'role', 'LPRphone', 'LPRemail', 'LPRlinkvk')
        }),
        ('Ссылки на музыкальные порталы', {
            'fields': ('linkYandexM', 'linkGoogleP', 'linkAppleM', 'linkYoutubeM')
        }),
        ('Ссылки группы', {
            'fields': ('linksite', 'linkvk', 'linkyoutube', 'linkinsta', 'linkfacebook')
        }),
    )
    inlines = [RelaseInLine, Group_MembersInLine, ManagementInLine, GalleryInLine, VideosInLine, PostersInLine]