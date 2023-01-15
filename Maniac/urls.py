from django.views.generic import RedirectView
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("MarketPlace.urls")),
    path('market/', include("MarketPlace.urls")),
    path('catalogofartists/', include("CatalogOfArtists.urls")),
    path('onlinemedia/', include("OnlineMedia.urls")),
    path('account/', include("account.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)