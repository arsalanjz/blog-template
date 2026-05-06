from typing import Required

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views import View

import accounts
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form_register = self.form_class()
        return render(request, self.template_name, {'form': form_register})


    def post(self, request):
        form_register = self.form_class(request.POST)
        if form_register.is_valid():
            cd_form = form_register.cleaned_data
            User.objects.create_user(cd_form['username'], cd_form['email'], cd_form['password'])
            messages.success(request, 'Account created for ' + cd_form['username'], 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form_register})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form_login = self.form_class()
        return render(request, self.template_name, {'form': form_login})

    def post(self, request):
        form_login = self.form_class(request.POST)
        if form_login.is_valid():
            cd_form = form_login.cleaned_data
            user = authenticate(username=cd_form['username'], password=cd_form['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful', 'success')
                return redirect('home:home')
            messages.error(request, 'Login unsuccessful,username or password wrong', 'danger')
        return render(request, self.template_name, {'form': form_login})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout successful', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,):
        user_posts = request.user.posts.all()
        context = {'posts': user_posts}
        return render(request, 'accounts/profile.html', context)


class UserPublicProfileView(View):
    def get(self,request,username,*args,**kwargs):
        target_user = get_object_or_404(User,username=username)
        user_posts = target_user.posts.all()
        context = {
            'target_user': target_user,
            'posts': user_posts
        }
        return render(request, 'accounts/profile.html', context)
