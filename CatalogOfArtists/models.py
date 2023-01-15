from django.db import models
from embed_video.fields import EmbedVideoField


class Genres(models.Model):
    GenreName = models.CharField(max_length=50, help_text='Жанр', verbose_name='Жанр')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.GenreName


class Cities(models.Model):
    CityName = models.CharField(max_length=60, help_text='Город', verbose_name='Город')

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.CityName


class Relase(models.Model):
    fk_artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40, verbose_name='Название релиза')
    image = models.ImageField(upload_to='images/photo_relases', blank=True, verbose_name='Изображение')
    age = models.CharField(max_length=4, verbose_name='Год выхода келиза')

    class Meta:
        verbose_name = 'релиз'
        verbose_name_plural = 'релизы'

    def __str__(self):
        return self.name


class Group_Members(models.Model):
    fk_artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, verbose_name='Фамилия, имя артиста')
    role = models.CharField(max_length=50, verbose_name='Роль музыканта в группе')

    class Meta:
        verbose_name = 'состав'
        verbose_name_plural = 'составы'

    def __str__(self):
        return self.name


class Management(models.Model):
    fk_artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    LPRname = models.CharField(max_length=100, help_text='Имя ЛПР (менеджер, директор и т.д.', verbose_name='Имя ЛПР')
    role = models.CharField(max_length=50, blank=True, help_text='Должность', verbose_name='Должность')
    LPRphone = models.CharField(max_length=13, help_text='Номер телефона ЛПР', verbose_name='Номер ЛПР')
    LPRemail = models.EmailField(help_text='Email ЛПР', null=True, verbose_name='email ЛПР')
    LPRlink = models.CharField(max_length=100, help_text='Cсылка на ЛПР', verbose_name='Ссылка ЛПР')

    class Meta:
        verbose_name = 'менеджмент'
        verbose_name_plural = 'менеджмент'


class Gallery(models.Model):
    fk_artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/gallery_artists', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галерея'


class Videos(models.Model):
    fk_artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    link = EmbedVideoField(max_length=200, help_text='Ссылка на видеозапись', verbose_name='Ссылка на видеозапись')

    class Meta:
        verbose_name = 'видеозапись'
        verbose_name_plural = 'видеозаписи'


class Poster(models.Model):
    fk_artist = models.ForeignKey('Artists', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/posters_artists', blank=True, verbose_name='Изображение')
    date = models.DateField(null=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'афиша'
        verbose_name_plural = 'афиша'


class Artists(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='images/photo_group', blank=True, verbose_name='Изображение')
    main_genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True, max_length=100,
                                   help_text='Введите основной жанр', verbose_name='Основной жанр',
                                   related_name='main_genre')
    genre = models.ManyToManyField(Genres, help_text='Выберите жанры', verbose_name='Жанры', related_name='genre')
    year_of_found = models.DateField(null=True, blank=True, verbose_name='Дата основания')
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, verbose_name='Город')
    text = models.TextField(max_length=10000, help_text='Введите информацию об артисте', verbose_name='Информация')
    vklink = models.CharField(max_length=100, help_text='ВК ссылка на артиста', verbose_name='Ссылка на вк')
    websitelink = models.CharField(max_length=100, help_text='Ссылка на сайт артиста', verbose_name='Веб-сайт')
    LPRname = models.CharField(max_length=100, help_text='Имя ЛПР (менеджер, директор и т.д.', verbose_name='Имя ЛПР')
    role = models.CharField(max_length=50, blank=True, help_text='Должность', verbose_name='Должность')
    LPRphone = models.CharField(max_length=13, help_text='Номер телефона ЛПР', verbose_name='Номер ЛПР')
    LPRemail = models.EmailField(help_text='Email ЛПР', null=True, verbose_name='email ЛПР')
    LPRlinkvk = models.CharField(max_length=100, help_text='ВК ссылка на ЛПР', verbose_name='Ссылка на вк ЛПР')
    feedback = models.BooleanField(default=True, verbose_name='Форма обратной связи')
    linkYandexM = models.CharField(max_length=100, blank=True, help_text='Ссылка на Яндекс.Музыка',
                                   verbose_name='Ссылка на Яндекс.Музыка')
    linkGoogleP = models.CharField(max_length=100, blank=True, help_text='Ссылка на Google Music',
                                   verbose_name='Ссылка на Google Music')
    linkAppleM = models.CharField(max_length=100, blank=True, help_text='Ссылка на Apple Music',
                                   verbose_name='Ссылка на Apple Music')
    linkYoutubeM = models.CharField(max_length=100, blank=True, help_text='Ссылка на YouTube Music',
                                   verbose_name='Ссылка на YouTube Music')
    linksite = models.CharField(max_length=100, blank=True, help_text='Ссылка на site',
                                    verbose_name='Ссылка на site')
    linkvk = models.CharField(max_length=100, blank=True, help_text='Ссылка на VK',
                                    verbose_name='Ссылка на VK')
    linkyoutube = models.CharField(max_length=100, blank=True, help_text='Ссылка на YouTube',
                                    verbose_name='Ссылка на YouTube')
    linkinsta = models.CharField(max_length=100, blank=True, help_text='Ссылка на Instagram',
                                    verbose_name='Ссылка на Instagram')
    linkfacebook = models.CharField(max_length=100, blank=True, help_text='Ссылка на Facebook',
                                    verbose_name='Ссылка на Facebook')

    class Meta:
        verbose_name = 'артист'
        verbose_name_plural = 'артисты'

    def __str__(self):
        return self.name

    def display_genre(self):
        return ', '.join([genre.GenreName for genre in self.genre.all()[:2]])

    display_genre.short_description = 'Жанр'
