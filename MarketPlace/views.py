from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, City, Element, Gallery, Tag, Poster, LinkList

def list_category(request):
    categories = Category.objects.all()

    context = {
        'categories' : categories,
    }
    templates = 'category/list_category.html'

    return render(request, templates, context)

def search_info(request):
    name_ = request.GET.get('name', '')
    cat__ = request.GET.get('cat', '')
    city_ = request.GET.get('city', '')

    elements = None

    try: # Система поиска информации по модулю веб-сайта
        if name_ and cat__ and city_: # Если введены все данные
            category = Category.objects.get(category_name=cat__)
            city = City.objects.get(city_name=city_)
            elements = Element.objects.filter(element_name=name_).filter(fk_category=category).filter(fk_city=city).all().order_by('-id')
        elif name_ and cat__: # Если введено название элемента и выбрано название категории
            category = Category.objects.get(category_name=cat__)
            elements = Element.objects.filter(element_name=name_).filter(fk_category=category).all().order_by('-id')
        elif name_ and city_: # Если введено название элемента и введено название города
            city = City.objects.get(city_name=city_)
            elements = Element.objects.filter(element_name=name_).filter(fk_city=city).all().order_by('-id')
        elif cat__ and city_: # Если выбрано название категории и введено название города
            category = Category.objects.get(category_name=cat__)
            city = City.objects.get(city_name=city_)
            elements = Element.objects.filter(fk_category=category).filter(fk_city=city).all().order_by('-id')
        elif name_ and not cat__ and not city_: # Если введено только название элемента
            elements = Element.objects.filter(element_name=name_).all().order_by('-id')
        elif not name_ and cat__ and not city_: # Если выбрано только название категории
            category = Category.objects.get(category_name=cat__)
            elements = Element.objects.filter(fk_category=category).all().order_by('-id')
        elif not name_ and not cat__ and city_: # Если введено только название города
            city = City.objects.get(city_name=city_)
            elements = Element.objects.filter(fk_city=city).all().order_by('-id')
    except: elements = None

    context = {
        'elements' : elements,
    }
    templates = 'category/search.html'

    return render(request, templates, context)

def list_elements(request, id):
    category = Category.objects.get(id=id)
    elements = Element.objects.filter(fk_category=id).all().order_by('-id')

    page = request.GET.get('page')
    paginator = Paginator(elements, 3)

    try:
        elements = paginator.page(page)
    except PageNotAnInteger:
        elements = paginator.page(1)
    except EmptyPage:
        elements = paginator.page(paginator.num_pages)

    context = {
        'elements' : elements,
        'category' : category,
    }
    templates = 'elements/list_elements.html'

    return render(request, templates, context)

def get_rating(request, id):
    element = Element.objects.get(id=id)

    element.rating += 1
    if element.rating > 5:
        element.rating = 5
    element.save()

    templates = 'elements/list_elements.html'

    return render(request, templates)

def info_element(request, id):
    element = Element.objects.get(id=id)
    gallery = Gallery.objects.filter(fk_element=element).all()
    posters = Poster.objects.filter(fk_element=element).all().order_by('-date')[:3]
    links = LinkList.objects.filter(fk_element=element).all()

    context = {
        'element' : element,
        'gallery' : gallery,
        'posters' : posters,
        'links' : links,
    }
    templates = 'elements/info_element.html'

    return render(request, templates, context)