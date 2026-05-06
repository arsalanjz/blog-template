from re import search

from django.contrib.postgres.search import SearchVector
from django.shortcuts import render , get_object_or_404
from django.views import View
from home.forms import SearchForm
from posts.models import Post
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank
from django.db.models.functions import Greatest


class PostListView(View):

    def get(self, request,):
        posts = Post.objects.all()
        search_form = SearchForm()
        if 'search' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd_search = form.cleaned_data['search']
                # posts = posts.filter(Q(title__icontains=cd_search) | Q(content__icontains=cd_search))
                posts = (posts.annotate(similarity=Greatest(
                    TrigramSimilarity('title' , cd_search ),
                    TrigramSimilarity('content' , cd_search) ))
                        .filter(similarity__gt=0.02).order_by('-similarity'))
                # vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
                # query = SearchQuery(cd_search)
                # posts = posts.annotate(Rank=SearchRank(vector, query)).filter(Rank__gte=0.1).order_by('-Rank')
                # search_title = (posts.annotate(similarity=TrigramSimilarity('title', cd_search),)
                #                 .filter(similarity__gt=0.1).order_by('-similarity'))
                # search_content = posts.filter(content__icontains=cd_search)
                # if search_title.exists():
                #     posts = search_title
                #     return render(request,'home/index.html',{'posts':posts, 'form':search_form})
                # if search_content.exists():
                #     posts = search_content
                #     return render(request,'home/index.html',{'posts':posts, 'form':search_form})



        return render(request,'home/index.html',{'posts':posts, 'form':search_form})
