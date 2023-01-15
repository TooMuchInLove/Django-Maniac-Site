from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Article,Section,News,Tag,Image,Header,Paragraph,Quote,Video
from account.models import Project
from account.my_decorators import project_member
from django.conf import settings
from .forms import ArticleHeader
from django.core.files.storage import FileSystemStorage #В конфигурации добавили кое что
from django.template.defaulttags import register


PICTURE_URL = "media/images/article_img/"


@project_member
def mediaform(request, id_project): #Отрисовка начальной формы + отрисовка доп полей
    case = 0
    position = 0
    tags = Tag.objects.all()
    project = Project.objects.get(id=id_project)
    try:   
        case = int(request.GET.get("upload"))
        position = int(request.GET.get("position"))

        if(case == 1):
            form = Header()
            position = position + 1
            template = "form_creator/fields.html"
        elif(case == 2):
            form = Paragraph()
            position = position + 1
            template = "form_creator/fields.html"
        elif(case == 3):
            form = Image()
            position = position + 1
            template = "form_creator/fields.html"
        elif(case == 4):
            form = Quote()
            position = position + 1
            template = "form_creator/fields.html"
        elif(case == 5):
            form = Video()
            position = position + 1
            template = "form_creator/fields.html"
        else:
            form = ArticleHeader()
            template = "form_creator/form_creator.html"

    except:
        form = ArticleHeader()
        template = "form_creator/form_creator.html"
    
    context = {
        "form" : form,
        "case" : case,
        "tags" : tags,
        "position": position,
        "project": project,
    }   
    return render(request, template, context)


def post(request, id_project=None):   #Пост-представление, разбирающее реквест

    title = request.POST.get("title") #Название статьи
    preview_text = request.POST.get("preview_text") #Описание статьи
    text = request.POST.get("text")

    image = request.FILES['image'] #Главное изображение. Просто жуть, достаём через реквест файл
    fs = FileSystemStorage(PICTURE_URL)
    filename = fs.save(image.name, image) #Сохраняем файл и берём линк
    # image_url = fs.url(filename)

    article = Article()
    article.preview_img = "images/article_img/" + filename
    article.title = title
    article.preview_text = preview_text
    article.text = text
    article.save()
    article.parts = 1

    category = request.POST.get("category")
    try:
        article.id_section = Section.objects.get(section_name_eng = category)
    except:
        pass

    tags = request.POST.getlist("tag")
    for tag in tags:
        try:
            article.tag.add(Tag.objects.get(tag_name = tag))
        except:
            pass

    for index in range(20):

        if(str(index) + ".header" in request.POST):
            text = request.POST.get(str(index) + ".header")
            header = Header()
            header.id_article = article
            header.text = text
            header.position = index
            header.save()
            article.parts = article.parts + 1
            

        if(str(index) + ".paragraph" in request.POST):
            text = request.POST.get(str(index) + ".paragraph")
            paragraph = Paragraph()
            paragraph.id_article = article
            paragraph.text = text
            paragraph.position = index
            paragraph.save()
            article.parts = article.parts + 1

        if(str(index) + ".quote" in request.POST):
            text = request.POST.get(str(index) + ".quote")
            quote = Quote()
            quote.id_article = article
            quote.quote = text
            quote.position = index
            quote.save()
            article.parts = article.parts + 1

        if(str(index) + ".image" in request.FILES):
            img = request.FILES[str(index) + ".image"]
            fs = FileSystemStorage(PICTURE_URL)
            filename = fs.save(img.name, img) 
            #image_url = fs.url(filename)
            
            image = Image()
            image.image = "images/article_img/" + filename
            image.id_article = article
            image.position = index
            image.save()
            article.parts = article.parts + 1

        if(str(index) + ".video" in request.POST):
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
    return HttpResponseRedirect(reverse("index-media", kwargs={'id_sec': 'all',
                                                               'id_tag': 'none',}))

