from django.contrib import admin
from .models import Category, City, Element, Gallery, Tag, Poster, LinkList


class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'category_name', )
admin.site.register(Category, CategoryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ( 'city_name', )
admin.site.register(City, CityAdmin)


class LinkListInline(admin.TabularInline):
    model = LinkList


class GalleryInline(admin.TabularInline):
    model = Gallery


class PosterInLine(admin.TabularInline):
    model = Poster


class TagInLine(admin.TabularInline):
    model = Tag


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    inlines      = [ LinkListInline, GalleryInline, PosterInLine, TagInLine ]
    list_display = ( 'element_name', 'element_phone', 'element_email' )
    list_filter  = ( 'fk_category_id', 'fk_city_id' )

    fieldsets = (
                  ( 'Список категорий и городов', { 'fields': ( 'fk_category', 'fk_city', ) } ),
                  ( 'Информация об элементе', { 'fields': ( 'element_name', 'element_address',
                                                            'element_preview_text', 'element_description',
                                                            'element_preview_img', 'element_phone',
                                                            'element_email', 'rating',
                                                            ( 'fact_value_1', 'fact_desc_1' ),
                                                            ( 'fact_value_2', 'fact_desc_2' ),
                                                            ( 'fact_value_3', 'fact_desc_3' ), ), } ),
                  ( 'Информация об ЛПР (лицо, принимающее решения)', { 'fields': ( 'LPR_name', 'LPR_phone',
                                                                                   'LPR_email', 'LPR_link_vk' ) } ),
    )