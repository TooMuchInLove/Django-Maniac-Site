from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from .models import Cities, Artists, Genres, Gallery, Videos, Poster
from .forms import EmailPostForm
import itertools


def index(request):
    genre = Genres.objects.all()
    artist = Artists.objects.all()
    i = 1
    var = ''
    for item in artist:
        var += item.name[0]
    # var = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    var = sorted(var)
    var = ''.join(ch for ch, _ in itertools.groupby(var))

    return render(
        request,
        'index.html',
        context={'genre': genre,
                 'artist': artist,
                'var': var,
        }
    )


def genre_detail_view(request, pk):
    artist = Artists.objects.filter(genre=pk).all()[:8]
    genre = Genres.objects.get(id=pk)
    template_name = 'genres_detail.html'

    return render(
        request,
        template_name,
        context={'genre': genre,
                 'artist': artist,
        }
    )


def artist_detail_view(request, pk):
    artist = Artists.objects.get(id=pk)
    gallery = Gallery.objects.filter(fk_artist=artist).all()
    posters = Poster.objects.filter(fk_artist=artist).all().order_by('-date')
    videos = Videos.objects.filter(fk_artist=artist).all()
    flaglink = True
    template_name = 'artists_card.html'
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            topic = 'Сообщение от пользователя сайта ({})'.format(cd['topic'])
            message = '{}\nОтвет по адресу {}'.format(cd['text'], cd['email'])
            send_mail(topic, message, 'testdjangos@gmail.com', [artist.LPRemail])
            return redirect('artist-card', pk)
        form = EmailPostForm()

    else:
        form = EmailPostForm()

    for item in videos:
        item.link = item.link.replace('watch?v=', 'embed/')


    if (artist.linkvk != '' or
        artist.linksite != '' or
        artist.linkvk != '' or
        artist.linkyoutube != '' or
        artist.linkinsta != '' or
        artist.linkfacebook != ''):
            flaglink = False



    context = {
        'artist': artist,
        'form': form,
        'flaglink': flaglink,
        'gallery': gallery,
        'videos': videos,
        'posters': posters,
    }
    return render(request, template_name, context)


# def artists_views(request):
#     artists = Artists.objects.all()
#     i = 1
#     var = ''
#     for item in artists:
#         var += item.name[0]
#     # var = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
#     var = sorted(var)
#     var = ''.join(ch for ch, _ in itertools.groupby(var))
#
#     context = {
#         'artists': artists,
#         'var': var,
#     }
#     template_name = 'artists_card.html'
#
#     return render(request, template_name, context)