from django.contrib import admin
from .models import Section,Article,Tag,News,Image,Header,Paragraph,Quote,Video

# Register your models here.
# class AuthorsAdmin(admin.ModelAdmin):
#     list_display = ('author_name',) #отображения хедеров в таблице
# admin.site.register(Authors,AuthorsAdmin)

class SectionsAdmin(admin.ModelAdmin):
    list_display = ('id','section_name','section_name_eng')
admin.site.register(Section,SectionsAdmin)

class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
admin.site.register(Tag,TagsAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_header',)
admin.site.register(News,NewsAdmin)

# class TypesAdmin(admin.ModelAdmin):
#     list_display = ('type_name',)
# admin.site.register(Types,TypesAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'id_section','id_project', 'preview_text',"preview_img" ,'create_date')
    list_filter = ('id_project', 'id_section')

    fieldsets = (
        ('Default info', {
            'fields' : (('id_section', 'id_project', 'tag'),) #'id_type'
        }),
        ('Page', {
            'fields' : (('preview_img','title','preview_text','text'))
        }),
        
    )

admin.site.register(Article,ArticleAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id_article','image',)
admin.site.register(Image,ImageAdmin)

class HeaderAdmin(admin.ModelAdmin):
    list_display = ('id_article','text',)
admin.site.register(Header,HeaderAdmin)

class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('id_article','text',)
admin.site.register(Paragraph,ParagraphAdmin)

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id_article','quote',)
admin.site.register(Quote,QuoteAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id_article','link',)
admin.site.register(Video,VideoAdmin)