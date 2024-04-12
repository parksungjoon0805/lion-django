from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.conf import settings
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, TodayArchiveView, TemplateView
from django.views.generic import FormView
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class PostLV(LoginRequiredMixin,ListView):
    login_url='/accounts/login/'
    model = Post
    template_name = "blog/post_all.html" 
    context_object_name = 'posts' 
    paginate_by = 3

    def get_queryset(self) :
        return self.model.objects.all()
    
def dummpy_post(request):
    objects = Post.objects.all()
    context={
        'posts' : objects
    }
    return render(request, "blog/post_all.html", context)


class PostDV(LoginRequiredMixin,DetailView):
    model=Post
    template_name="blog/post_detail.html"

    # def get_object(self):
    #     pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url']= f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context


#--- ArchiveView
class PostAV(LoginRequiredMixin,ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'
    template_name = "blog/post_archive.html"


class PostYAV(LoginRequiredMixin,YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True
    template_name = "blog/post_archive_year.html"



class PostMAV(LoginRequiredMixin,MonthArchiveView):
    model = Post
    date_field = 'modify_dt'
    template_name = "blog/post_archive_month.html"



class PostDAV(LoginRequiredMixin,DayArchiveView):
    model = Post
    date_field = 'modify_dt'
    template_name = "blog/post_archive_day.html"



class PostTAV(LoginRequiredMixin,TodayArchiveView):
    model = Post
    date_field = 'modify_dt'
    template_name = "blog/post_archive_day.html"

class TagCloudTV(LoginRequiredMixin,TemplateView):
    template_name="taggit/taggit_cloud.html"

class TaggedObjectLV(LoginRequiredMixin,ListView):
    template_name='taggit/taggit_post_list.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
    
   
# -----FormView
class SearchFormView(LoginRequiredMixin,FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord=form.cleaned_detail['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__post_list = searchWord)
                                        | Q(content__icontains=searchWord)).distinct()
        
        context={}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)