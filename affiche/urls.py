from dal import autocomplete
from django.urls import path

from .models import Performers
from .views import (index_page_view, performance_detail_page_view, backstage_page_view, backstage_detail_page_view,
                    repertory_page_view, repertory_detail_page_view, hall_view, CreativeAutocomplete,
                    ConductorAutocomplete, PerformerAutocomplete)

urlpatterns = [
    path('', index_page_view, name='index'),
    path('<int:pk>/', performance_detail_page_view, name='performance_detail'),
    path('backstage/', backstage_page_view, name='backstage'),
    path('backstage/<int:backstage_pk>/', backstage_detail_page_view, name='backstage_detail'),
    path('repertory/', repertory_page_view, name='repertory'),
    path('repertory/<int:performance_pk>', repertory_detail_page_view, name='repertory_detail'),
    path('hall/<int:pk>/', hall_view, name='hall'),
    path('creative-autocomplete/', CreativeAutocomplete.as_view(), name='creative-autocomplete'),
    path('performer-autocomplete/', PerformerAutocomplete.as_view(), name='performer-autocomplete'),
    path('conductor-autocomplete/', ConductorAutocomplete.as_view(), name='conductor-autocomplete'),
]
