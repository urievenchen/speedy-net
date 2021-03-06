from django.urls import path

from . import views
from speedy.core.accounts.urls import urlpatterns

app_name = 'speedy.match.accounts'
urlpatterns = [
    path(route='', view=views.IndexView.as_view(), name='index'),
    path(route='welcome/', view=views.ActivateSiteProfileView.as_view(), name='activate'),
    path(route='registration-step-<digits:step>/', view=views.ActivateSiteProfileView.as_view(), name='activate'),
    path(route='edit-profile/notifications/', view=views.EditProfileNotificationsView.as_view(), name='edit_profile_notifications'),
] + urlpatterns


