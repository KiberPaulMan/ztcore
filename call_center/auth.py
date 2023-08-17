from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('incoming_calls')
                else:
                    return HttpResponse('Аккаунт не является действительным')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Неверно введен логин или пароль. Пожалуйста, попробуйте снова.'
                                     )
    else:
        form = LoginForm()
    return render(request, 'call_center/registration/login.html', {'form': form})
