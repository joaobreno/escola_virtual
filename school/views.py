from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import *
from .decorator import *

def index(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    redirect_url = reverse('home', args=[])
                    return HttpResponseRedirect(redirect_url)
                else:
                    messages.error(request, 'Email ou senha inválidos.')
        else:
            form = LoginForm()

        return render(request, 'index.html', {'form': form})
    
    else:
        redirect_url = reverse('home', args=[])
        return HttpResponseRedirect(redirect_url)


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)  
                messages.success(request, f'Conta criada com sucesso para {user.username}!')
                redirect_url = reverse('home', args=[])
                return HttpResponseRedirect(redirect_url)
            else:
                messages.error(request, 'Ocorreu um erro no cadastro. Verifique os campos abaixo.')
        else:
            form = UserRegisterForm()
    else:
        redirect_url = reverse('home', args=[])
        return HttpResponseRedirect(redirect_url)

    return render(request, 'signup.html', {'form': form})


@login_required(login_url='index')
@profile_user
def home(request, context_dict):
    # if request.method == 'POST':
    #     profile_form = ProfileForm(request.POST, request.FILES)
    #     if profile_form.is_valid():
    #         profile = context_dict['profile']

    #         profile.name = profile_form.cleaned_data['name']
    #         profile.about = profile_form.cleaned_data['about']
    #         profile.job = profile_form.cleaned_data['job']
    #         profile.country = profile_form.cleaned_data['country']
    #         profile.address = profile_form.cleaned_data['address']
    #         profile.phone = profile_form.cleaned_data['phone']
    #         profile.email = profile_form.cleaned_data['email']
    #         profile.facebook = profile_form.cleaned_data['facebook']
    #         profile.instagram = profile_form.cleaned_data['instagram']
    #         profile.linkedin = profile_form.cleaned_data['linkedin']

    #         profile.profile_photo = profile_form.cleaned_data['profile_photo']

    #         profile.save()
    #         messages.success(request, 'Alterações do perfil salvas com sucesso!')
    #         return redirect('profile')
    #     else:
    #         messages.error(request, 'Erro no formulário!')
    # else:
    #     profile_form = ProfileForm(profile=context_dict['profile'])
        
    # trees_registered = PlantedTree.objects.filter(user=request.user).order_by('-planted_at')
    # accounts = request.user.accounts.all()

    # context_dict['profile_form'] = profile_form
    # context_dict['planted_trees'] = trees_registered
    # context_dict['number_trees'] = len(trees_registered)
    # context_dict['accounts'] = accounts
    # context_dict['number_accounts'] = len(accounts)
    return render(request, 'home.html', context_dict)



def quick_logout(request):
    logout(request)
    return redirect('index')