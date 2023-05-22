from django.urls import path
from . import views


# {DOMAIN}/brewery/
urlpatterns = [
    path('', views.BreweryView.as_view(), name='brewery_view'),
    path('<int:brewery_id>/', views.BreweryDetailView.as_view(), name='brewery_detail_view'),
]