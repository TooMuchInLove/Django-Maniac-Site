from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from datetime import date
from uuid import uuid4

# *** Market Place ***

class Category(models.Model):
    """ Categories """
    category_name = models.CharField(max_length=300, unique=True, verbose_name='Название категории',
                                     help_text='( Введите название категории )')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.category_name


class City(models.Model):
    """ Cities """
    city_name = models.CharField(max_length=100, unique=True, verbose_name='Название города',
                                 help_text='( Введите название города )')

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.city_name


class Element(models.Model):
    """ Elements """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: \'+999999999\'. Up to 15 digits allowed.')

    fk_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категориия',
                                    help_text='( Выберите категорию из списка )')
    fk_city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Город',
                                help_text='( Выберите город из списка )')

    element_name = models.CharField(max_length=300, unique=False, verbose_name='Название элемента',
                                    help_text='( Введите название элемента )')
    element_address = models.CharField(max_length=300, blank=True, verbose_name='Адрес элемента',
                                       help_text='( Введите адрес элемента )')
    element_preview_text = models.TextField(max_length=1000, blank=True, verbose_name='Краткое описание',
                                            help_text='( Введите краткое описание элемента )')
    element_description = models.TextField(blank=True, verbose_name='Подробное описание',
                                           help_text='( Введите подробное описание элемента )')
    element_preview_img = models.ImageField(upload_to='images/elements', height_field=None, width_field=None,
                                            max_length=100, blank=True, verbose_name='Картинка элемента')
    element_phone = models.CharField(validators=[ phone_regex ], max_length=17, blank=True,
                                     verbose_name='Номер телефона', help_text='( Номер телефона в формате: +999999999 )')
    element_email = models.EmailField(max_length=254, unique=True, blank=True, verbose_name='Электронный адрес элемента',
                                      help_text='( Добавьте адрес электронной почты )')
    fact_value_1 = models.CharField(max_length=100, blank=True, verbose_name='Значение факта для элемента',
                                    help_text='( Введите значение факта [1] для элемента )')
    fact_desc_1 = models.CharField(max_length=100, blank=True, verbose_name='Описание факта для элемента',
                                   help_text='( Введите описание факта [1] для элемента )')
    fact_value_2 = models.CharField(max_length=100, blank=True, verbose_name='Значение факта для элемента',
                                    help_text='( Введите значение факта [2] для элемента )')
    fact_desc_2 = models.CharField(max_length=100, blank=True, verbose_name='Описание факта для элемента',
                                   help_text='( Введите описание факта [2] для элемента )')
    fact_value_3 = models.CharField(max_length=100, blank=True, verbose_name='Значение факта для элемента',
                                    help_text='( Введите значение факта [3] для элемента )')
    fact_desc_3 = models.CharField(max_length=100, blank=True, verbose_name='Описание факта для элемента',
                                   help_text='( Введите описание факта [3] для элемента )')
    rating = models.IntegerField(default=0, null=True, blank=True)

    LPR_name = models.CharField(max_length=100, verbose_name='ФИО',
                                help_text='( Введите ФИО )')
    LPR_phone = models.CharField(validators=[ phone_regex ], max_length=17, blank=True,
                                 verbose_name='Номер телефона', help_text='( Номер телефона в формате: +999999999 )')
    LPR_email = models.EmailField(max_length=254, unique=True, blank=True, verbose_name='Электронный адрес элемента',
                                  help_text='( Добавьте адрес электронной почты )')
    LPR_link_vk = models.CharField(max_length=300, blank=True, verbose_name='Ссылка на ВК',
                                   help_text='( Добавьте ссылку на сообщество в ВК )')

    class Meta:
        verbose_name = 'элемент'
        verbose_name_plural = 'элементы'

    def __str__(self):
        return self.element_name


class LinkList(models.Model):
    """ Link list for element """
    fk_element = models.ForeignKey('Element', on_delete=models.CASCADE, null=True)
    element_link = models.CharField(max_length=300, blank=True, verbose_name='Ссылка на элемент')

    class Meta:
        verbose_name = 'ссылка на элемент'
        verbose_name_plural = 'ссылка на элемент'


class Gallery(models.Model):
    """ Gallery for element """
    fk_element = models.ForeignKey('Element', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/gallery', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галерея'


class Poster(models.Model):
    """ Posters for element """
    fk_element = models.ForeignKey('Element', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/posters', blank=True, verbose_name='Изображение')
    date = models.DateField(null=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'афиша'
        verbose_name_plural = 'афиша'


class Tag(models.Model):
    """ Tags for element """
    fk_element = models.ForeignKey('Element', on_delete=models.CASCADE, null=True)
    tag_name = models.CharField(max_length=100, unique=True, verbose_name='Название тэга',
                                help_text='( Введите название тэга )')
    tag_desc = models.TextField(blank=True, verbose_name='Подробное описание',
                                help_text='( Введите подробное описание тэга )')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.tag_name