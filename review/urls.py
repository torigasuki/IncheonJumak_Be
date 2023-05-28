from django.urls import path
from review import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<int:user_id>/reviews/', views.ShowMyReview.as_view(), name='review_filtering_view'),

    path('alcohol/', views.Alcohol_ReviewView.as_view(), name='alcohol_review_view'),
    path('alcohol/<int:alchol_id>/', views.Alcohol_ReviewView.as_view(), name='alcohol_review_detail_view'),
    path('alcoholreview/<int:review_id>/', views.Alcohol_ReviewView.as_view(), name='alcohol_review_delete_view'),

    path('brewery/', views.Brewery_ReviewView.as_view(), name='brewery_review_view'),
    path('brewery/<int:brewery_id>/', views.Brewery_ReviewView.as_view(), name='brewery_review_detail_view'),
    path('breweryreview/<int:review_id>/', views.Brewery_ReviewView.as_view(), name='brewery_review_delete_view'),

    path('event/', views.Event_ReviewView.as_view(), name='event_review_view'),
    path('event/<int:event_id>/', views.Event_ReviewView.as_view(), name='event_review_detail_view'),
    path('eventreview/<int:review_id>/', views.Event_ReviewView.as_view(), name='event_review_delete_view'),

    # path('comment/', views.CommentView.as_view(), name='comment_view'),
    # path('comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'),
    # path('like/', views.LikeView.as_view(), name='like_view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)