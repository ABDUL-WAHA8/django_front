from django.urls import path
from . import views

#url conf

urlpatterns=[
    path("/tests_likes",views.test_likes)
]