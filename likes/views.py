from django.shortcuts import render
from django.http import HttpRequest
from likes.models import LikedItem

def test_likes(request):
    likes=LikedItem.objects.all()
    print(likes)
    return render(request,"liker.html")

