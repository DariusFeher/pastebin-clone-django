from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from .views import (PastebinDetailView, PastebinsView, clone_pastebin_create,
                    clone_pastebin_delete, clone_pastebin_edit)

app_name = 'pastes'

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', PastebinsView.as_view(), name='list'),
	path('pastebins/new/', clone_pastebin_create, name='new'),
	path('pastebins/<pk>/', PastebinDetailView.as_view(), name='detail'),
	path('pastebins/<pk>/delete/', clone_pastebin_delete, name='delete'),
	path('pastebins/<pk>/edit/', clone_pastebin_edit, name='edit')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)