import logging
from datetime import date

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views import generic

from plan import forms
from plan.models import Account

logger = logging.getLogger('planndit.views')


class IndexView(generic.TemplateView):
    template_name = 'plan/base.html'


class TestView(generic.TemplateView):
    template_name = 'plan/test.html'


class Login(generic.TemplateView):
    template_name = 'plan/login.html'

    def post(self, request, **kwargs):
        form = forms.LoginForm(request.POST)
        username = request.POST['login']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('plan:index'))
            else:
                error = "Username or Password is incorrect"
        else:
            error = form.errors.as_text()
        logger.warning(error)
        return render(request, self.template_name, {
            'error': error,
            'login': username,
            'password': password,
        })
        # logger.log(password)


class Logout(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('plan:index'))


class Register(generic.TemplateView):
    template_name = 'plan/register.html'

    def post(self, request, **kwargs):
        form = forms.RegisterForm(request.POST)
        username = request.POST['login']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        if form.is_valid():
            if password == password_repeat:
                user = User.objects.create_user(username=username, password=password)
                user.account = Account.objects.create(user_id=user.id)
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('plan:index'))

        error = form.errors.as_text()
        logger.warning(error)
        return render(request, self.template_name, {
            'error': error,
            'login': username,
            'password': password,
        })
        # logger.log(password)


