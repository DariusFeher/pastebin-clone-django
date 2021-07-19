from django.urls import path

from .views import (PastebinDetailView, PastebinsView, clone_pastebin_create,
                    clone_pastebin_delete, clone_pastebin_edit)

app_name = 'clone_pastebin'

urlpatterns = [
	path('', PastebinsView.as_view(), name='list'),
	path('pastebins/new/', clone_pastebin_create, name='new'),
	path('pastebins/<pk>/', PastebinDetailView.as_view(), name='detail'),
	path('pastebins/<pk>/delete/', clone_pastebin_delete, name='delete'),
	path('pastebins/<pk>/edit/', clone_pastebin_edit, name='edit')
]
