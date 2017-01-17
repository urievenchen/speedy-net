from django.conf import settings
from django.conf.urls import url, include

from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('speedy.match.accounts.urls', namespace='accounts')),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^about/', include('speedy.core.about.urls', namespace='about')),
    url(r'^privacy/', include('speedy.core.privacy.urls', namespace='privacy')),
    url(r'^terms/', include('speedy.core.terms.urls', namespace='terms')),
    url(r'^contact/', include('speedy.core.feedback.urls', namespace='feedback')),

    # always at the bottom
    url(r'^(?P<slug>[-\._\w]+)/friends/', include('speedy.core.friends.urls', namespace='friends')),
    url(r'^messages/', include('speedy.core.im.urls_private', namespace='im')),
    url(r'^messages/(?P<slug>[-\._\w]+)/', include('speedy.core.im.urls_public', namespace='im_entity')),
    url(r'^(?P<slug>[-\._\w]+)/blocks/', include('speedy.core.blocks.urls', namespace='blocks')),
    url(r'^(?P<slug>[-\._\w]+)/likes/', include('speedy.match.likes.urls', namespace='likes')),
    url(r'^uploads/', include('speedy.core.uploads.urls', namespace='uploads')),
    url(r'^', include('speedy.core.profiles.urls', namespace='profiles')),
]

if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns

try:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
except ImportError:
    pass
