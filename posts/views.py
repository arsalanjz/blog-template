from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView

from posts.forms import PostForm
from posts.models import Post
from django.contrib import messages


class PostDetailView(View):

    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, id=post_id, slug=post_slug)
        return render(request, 'posts/post_detail.html', {'post': post})


class PostCreateView(LoginRequiredMixin,View):
    form_class = PostForm
    template_name = 'posts/create_post.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'cant create post,you not admin','danger')
            return redirect('accounts:profile_user')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form_create_post = self.form_class
        return render(request, self.template_name, {'form': form_create_post})

    def post(self, request, *args, **kwargs):
        form_create_post = self.form_class(request.POST)
        if form_create_post.is_valid():
            cd_form = form_create_post.cleaned_data
            Post.objects.create(author=request.user,**cd_form)
            messages.success(request,'successfully created post,success')
            return redirect('accounts:profile_user')
        return render(request, self.template_name, {'form_create_post': form_create_post})


class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostForm
    template_name = 'posts/update_post.html'

    def dispatch(self, request, *args, **kwargs,):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if not post.author.id == request.user.id:
            messages.error(request, 'cant update this post,you not owner this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,post_id):
        post = Post.objects.get(pk=post_id)
        form_update_post = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form_update_post})
    def post(self, request,post_id):
        post = Post.objects.get(pk=post_id)
        form_update_post = self.form_class(request.POST,instance=post)
        if form_update_post.is_valid():
            form_update_post.save(commit=False)
            post.slug=slugify(form_update_post.cleaned_data['title'])
            form_update_post.save()
            messages.success(request,'successfully updated post','success')
            return redirect('accounts:profile_user')
        messages.error(request,'you cant update this post','danger')
        return render(request, self.template_name, {'form': form_update_post})





class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request, post_id,):
        post = get_object_or_404(Post, id=post_id)
        if post.author.id == request.user.id:
            post.delete()
            messages.success(request,'successfully deleted post,success')
        else:
            messages.error(request,'you cant delete this post','danger')
        return redirect('accounts:profile_user')

