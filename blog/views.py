from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.views.generic import ListView


class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 1
