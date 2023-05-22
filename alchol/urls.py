from django.urls import path
from . import views


# {DOMAIN}/alchol/
urlpatterns = [
    path('', views.AlcholView.as_view(), name='alchol_view'),
    path('category/<str:sort>/', views.AlcholCategoryView.as_view(), name='alchol_category_view'),
    path('<int:alchol_id>/', views.AlcholDetailView.as_view(), name='alchol_detail_view'),
]