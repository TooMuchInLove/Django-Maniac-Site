from django.shortcuts import render,reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Article,Section,News,Tag,Image,Header,Paragraph,Quote,Video
from account.models import Project
from account.my_decorators import is_member_posting
from django.conf import settings
from .forms import ArticleHeader
from django.core.files.storage import FileSystemStorage #В конфигурации добавили кое что
from django.template.defaulttags import register


PICTURE_URL = "media/images/article_img/"


@register.filter  # добавляем фильтр для шаблонизатора Пример добавления к декоратору
def get_range(value):
    return list(range(value))


@is_member_posting
def mediaform_editor(request, id_project=None, id_article=None):  # Отрисовка начальной формы + отрисовка доп полей

    case = 0
    position = 0
    project = Project.objects.get(id=id_project)
    # Общие элементы
    tags = Tag.objects.all()
    sections = Section.objects.all()
    # Элементы формы
    article = Article.objects.get(id=id_article)
    article_images = Image.objects.filter(id_article=id_article)
    article_headers = Header.objects.filter(id_article=id_article)
    article_paragraphs = Paragraph.objects.filter(id_article=id_article)
    article_quotes = Quote.objects.filter(id_article=id_article)
    article_videos = Video.objects.filter(id_article=id_article)
    article_tags = article.tag.all()  # Many-to-Many
    article_section = Section.objects.get(id=article.id_section.id)

    template = 'smi-detail.html'

    for item in article_videos:
        item.link = item.link.replace('watch?v=', 'embed/')  # Странно работает, от Егора

    # Подгрузка полей при обращении от AJAX

    try:
        case = int(request.GET.get("upload"))
        position = int(request.GET.get("position"))

        if (case == 1):
            form = Header()
            position = position + 1
            template = "form_creator/fields.html"
        elif (case == 2):
            form = Paragraph()
            position = position + 1
            template = "form_creator/fields.html"
        elif (case == 3):
            form = Image()
            position = position + 1
            template = "form_creator/fields.html"
        elif (case == 4):
            form = Quote()
            position = position + 1
            template = "form_creator/fields.html"
        elif (case == 5):
            form = Video()
            position = position + 1
            template = "form_creator/fields.html"
        else:
            # form = ArticleHeader()
            template = "form_creator/form_editor.html"

    except:
        # form = ArticleHeader()
        template = "form_creator/form_editor.html"

    context = {
        'project': project,
        'article': article,  # Данные о статье
        'article_section': article_section,
        'article_images': article_images,
        'article_headers': article_headers,
        'article_paragraphs': article_paragraphs,
        'article_quotes': article_quotes,
        'article_videos': article_videos,
        'article_tags': article_tags,

        # Общие данные
        'MEDIA_URL': settings.MEDIA_URL,
        # "form": form,
        "case": case,
        "sections": sections,
        "tags": tags,
        "position": position,
        "project": project,
        "id_article": id_article,

    }

    return render(request, template, context)


def post_edit(request, id_project=None, id_article=None):  # Пост-представление, разбирающее реквест

    article = Article()
    article_delete = Article.objects.get(id=id_article)

    title = request.POST.get("title")  # Название статьи
    preview_text = request.POST.get("preview_text")  # Описание статьи
    text = request.POST.get("text")
    if('first_image' in request.FILES ):
        image = request.FILES['first_image']  # Главное изображение. Просто жуть, достаём через реквест файл
        fs = FileSystemStorage(PICTURE_URL)
        filename = fs.save(image.name, image)  # Сохраняем файл и берём линк, Убираем пробелы в названии
        article.preview_img = "images/article_img/" + filename
    else:
        article.preview_img = article_delete.preview_img
        # image_url = fs.url(filename)



    article.title = title
    article.preview_text = preview_text
    article.text = text
    article.save()
    article.parts = 1

    category = request.POST.get("category")
    try:
        article.id_section = Section.objects.get(section_name_eng=category)
    except:
        pass

    tags = request.POST.getlist("tag")
    for tag in tags:
        try:
            article.tag.add(Tag.objects.get(tag_name=tag))
        except:
            pass

    for index in range(20):

        if (str(index) + ".header" in request.POST):
            text = request.POST.get(str(index) + ".header")
            header = Header()
            header.id_article = article
            header.text = text
            header.position = index
            header.save()
            article.parts = article.parts + 1

        if (str(index) + ".paragraph" in request.POST):
            text = request.POST.get(str(index) + ".paragraph")
            paragraph = Paragraph()
            paragraph.id_article = article
            paragraph.text = text
            paragraph.position = index
            paragraph.save()
            article.parts = article.parts + 1

        if (str(index) + ".quote" in request.POST):
            text = request.POST.get(str(index) + ".quote")
            quote = Quote()
            quote.id_article = article
            quote.quote = text
            quote.position = index
            quote.save()
            article.parts = article.parts + 1

        if (str(index) + ".image" in request.FILES):

            img = request.FILES[str(index) + ".image"]
            fs = FileSystemStorage(PICTURE_URL)
            filename = fs.save(img.name, img)
            # image_url = fs.url(filename)

            image = Image()
            image.image = "images/article_img/" + filename
            image.id_article = article
            image.position = index
            image.save()
            article.parts = article.parts + 1
        elif(str(index) + ".image" in request.POST): #Если в форму не закинута картинка
            image = Image()
            image.image = Image.objects.get(id_article=article_delete,position=index).image
            image.id_article = article
            image.position = index
            image.save()
            article.parts = article.parts + 1

        if (str(index) + ".video" in request.POST):
            link = request.POST.get(str(index) + ".video")
            quote = Video()
            quote.id_article = article
            quote.link = link
            quote.position = index
            quote.save()
            article.parts = article.parts + 1

    project = Project.objects.get(id=id_project)
    article.id_project = project
    article.save()
    article_delete.delete()
    return HttpResponseRedirect(reverse("index-media", kwargs={'id_sec': 'all',
                                                                   'id_tag': 'none',}))