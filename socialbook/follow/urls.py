# follow/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('follow/<str:username>/', FollowView.as_view(), name='follow_user'),
    path('followers/', FollowersListView.as_view(), name='followers'),
    path('following/', FollowingListView.as_view(), name='following'),
    path('search/', UserSearchView.as_view(), name='user_search'),

]
