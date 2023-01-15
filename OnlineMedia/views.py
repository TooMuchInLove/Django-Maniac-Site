from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Article, Section, News, Tag, Image, Header, Paragraph, Quote, Video
# from django.views.generic import View,DetailView,ListView
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.defaulttags import register


@register.filter  # добавляем фильтр для шаблонизатора Пример добавления к декоратору
def get_range(value):
    return list(range(value))


def article_list(request, id_sec="all", id_tag="none"):
    # Костыльно считаем число статей в секциях
    # Индексы к секциям идут строго по порядку
    url_section = id_sec
    
    if id_tag != "none":
        tag = Tag.objects.get(id=id_tag)

    if id_sec == "all":
        if id_tag != "none":
            articles = Article.objects.order_by('-create_date', '-create_time').filter(tag=tag)
        else:
            articles = Article.objects.order_by('-create_date', '-create_time')
    else:
        id_sec = Section.objects.get(section_name_eng=id_sec)
        # Переопределяем переменную чтобы по ключу секции взять нужные картинки
        
        if id_tag != "none":
            articles = Article.objects.filter(id_section=id_sec).order_by('create_date').order_by('create_time')\
                .filter(tag=tag)
        else:
            articles = Article.objects.filter(id_section=id_sec).order_by('create_date').order_by('create_time')
    
    # Пагинация

    page = request.GET.get('page')
    paginator = Paginator(articles, 3)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # Пагинация

    tags = []
    for article in articles:
        for tag in article.tag.all():
            if not(tag in tags):
                tags.append(tag)

    sections = Section.objects.all()  # Берём все секции и новости
    news = News.objects.order_by('-news_date')[:3]
    template = 'smi.html'

    context = {
        'sections': sections,
        'articles': articles,
        'news': news,
        'tags': tags,
        'url_section': url_section,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, template, context)


def article_detail(request, id_art, id_sec):
    sections = Section.objects.all()
    news = News.objects.order_by('-news_date')[:3]
    try:
        article = Article.objects.get(id=id_art)
    except():
        return HttpResponseRedirect('page_not_found')
    article.views = article.views+1
    article.save()

    images = Image.objects.filter(id_article=id_art)
    headers = Header.objects.filter(id_article=id_art)
    paragraphs = Paragraph.objects.filter(id_article=id_art)
    quotes = Quote.objects.filter(id_article=id_art)
    videos = Video.objects.filter(id_article=id_art)
    tags = Tag.objects.all()[:20]

    template = 'smi-detail.html'

    for item in videos:
        item.link = item.link.replace('watch?v=', 'embed/')

    context = {
        'sections': sections,
        'article': article,
        'news': news,
        'images': images,
        'headers': headers,
        'paragraphs': paragraphs,
        'quotes': quotes,
        'videos': videos,
        'tags': tags,
        'url_section': id_sec,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, template, context)


def news_detail(request, id_news):

    news_item = News.objects.get(id=id_news)
    news = News.objects.order_by('-news_date')[:3]
    tags = Tag.objects.all()[:20]
    template = 'news-detail.html'
    sections = Section.objects.all()

    context = {
        'sections': sections,
        'news_item': news_item,
        'news': news,
        'tags': tags,
        # 'MEDIA_URL' : settings.MEDIA_URL,
    }
    return render(request, template, context)


def page_not_found(request):
    news = News.objects.order_by('-news_date')[:3]
    sections = Section.objects.all()
    tags = Tag.objects.all()[:20]

    context = {
        'news': news,
        'sections': sections,
        'tags': tags,
    }
    template = "page_not_found.html"
    return render(request, template, context)

# class Article_List(ListView):
#     model = Articles

# Create your views here.
