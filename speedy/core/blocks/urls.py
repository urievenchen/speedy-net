from django.urls import path

from . import views

app_name = 'speedy.core.blocks'
urlpatterns = [
    path(route='block/', view=views.BlockView.as_view(), name='block'),
    path(route='unblock/', view=views.UnblockView.as_view(), name='unblock'),
]


