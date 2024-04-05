from django.shortcuts import render
from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark
# Create your views here.

class BookmarkLV(ListView):
    model=Bookmark

    # template_name="bookmark/bookmark_list.html"
    # content_object_name="object_list"
    pass

class BookmarkDV(DetailView):
    model=Bookmark
    # template_name = 'bookmark/bookmark_detail.html'
    # context_object_name = 'object'
    pass
