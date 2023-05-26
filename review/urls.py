from django.urls import path
from review import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ReviewView.as_view(), name='review_view'),
    path('<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
    #user id로 filtering review list
    path('<int:user_id>/reviews/', views.ReviewFilteringUserView.as_view(), name='review_filtering_view'),
    path('comment/', views.CommentView.as_view(), name='comment_view'),
    path('comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'),
    path('like/', views.LikeView.as_view(), name='like_view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)