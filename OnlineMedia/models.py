from django.db import models
from account.models import Project
from embed_video.fields import EmbedVideoField


ID = 1


class Tag(models.Model):
    tag_name = models.CharField(max_length=50,
                                unique=True,
                                verbose_name="Название тега")

    tag_desc = models.CharField(max_length=255,
                                verbose_name="Описание тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag_name


class News(models.Model):
    news_header = models.CharField(max_length=50,
                                   unique=True,
                                   verbose_name="Краткая статья")

    news_text = models.TextField(unique=True,
                                 verbose_name="Текст новости")

    news_date = models.DateField(verbose_name="Дата новости")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.news_header


class Section(models.Model):
    section_name = models.CharField(max_length=80,
                                    unique=True,
                                    help_text="Название раздела",
                                    verbose_name="Раздел")

    section_name_eng = models.CharField(max_length=80,
                                        default="name",
                                        help_text="Название раздела",
                                        verbose_name="Раздел на инглише")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.section_name
        

class Article(models.Model):
    id_section = models.ForeignKey(Section,
                                   on_delete=models.CASCADE,
                                   help_text="Идентификатор категории",
                                   verbose_name="Категория",
                                   blank=True,
                                   null=True)

    id_project = models.ForeignKey(Project,
                                   on_delete=models.CASCADE,
                                   help_text="Идентификатор проекта",
                                   verbose_name="Проект",
                                   blank=True,
                                   null=True)

    # id_type = models.ForeignKey(Types, on_delete = models.SET_NULL, verbose_name="Вид статьи", null = True)
    title = models.TextField(max_length=80,
                             help_text="Заголовок статьи",
                             verbose_name="Заголовок")

    preview_text = models.TextField(max_length=300,
                                    help_text="Краткое описание",
                                    verbose_name="Краткое описание")

    preview_img = models.ImageField(help_text="Картинка для статьи в списке",
                                    upload_to="images/article_img",
                                    verbose_name="Картинка")

    text = models.TextField(max_length=3000,
                            help_text="Полный текст статьи",
                            verbose_name="Текст")

    create_date = models.DateField(help_text="Дата написания статьи",
                                   verbose_name="Дата",
                                   auto_now_add=True,)

    create_time = models.TimeField(help_text="Время написания статьи",
                                   verbose_name="Время",
                                   auto_now_add=True,)

    tag = models.ManyToManyField(to="Tag")

    views = models.IntegerField(default=0,
                                help_text="Просмотры")

    parts = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title  # self.id_project.name +" "+ self.title

# ниже элементы статьи


class Image(models.Model):
    id_article = models.ForeignKey("Article",
                                   verbose_name="Статья",
                                   on_delete=models.CASCADE,
                                   default=ID)

    image = models.ImageField(upload_to="images/article_img",
                              help_text="Картинка")

    about = models.TextField(verbose_name="Заголовок",
                             max_length=300)

    position = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return str(self.image)


class Header(models.Model):
    id_article = models.ForeignKey("Article",
                                   verbose_name="Статья",
                                   on_delete=models.CASCADE,
                                   default=ID)

    text = models.CharField(verbose_name="Заголовок",
                            max_length=200)

    position = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "Заголовки"

    def __str__(self):
        return str(self.text)


class Paragraph(models.Model):
    id_article = models.ForeignKey("Article",
                                   verbose_name="Статья",
                                   on_delete=models.CASCADE,
                                   default=ID)

    text = models.TextField(verbose_name="Параграф",
                            max_length=3000)

    position = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Абзац"
        verbose_name_plural = "Абзацы"

    def __str__(self):
        return str(self.text)


class Quote(models.Model):
    id_article = models.ForeignKey("Article",
                                   verbose_name="Статья",
                                   on_delete=models.CASCADE,
                                   default=ID)

    quote = models.TextField(verbose_name="Цитата",
                             max_length=1000)

    quoter = models.TextField(verbose_name="Кто сказал",
                              max_length=100)

    position = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    def __str__(self):
        return str(self.quote)


class Video(models.Model):
    id_article = models.ForeignKey("Article",
                                   verbose_name="Статья",
                                   on_delete=models.CASCADE,
                                   default=ID)

    link = EmbedVideoField(max_length=200,
                           help_text='Ссылка на видеозапись',
                           verbose_name='Ссылка на видеозапись')

    position = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return str(self.link)
