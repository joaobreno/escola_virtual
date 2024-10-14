from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import *
from .decorator import *
from .models import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import EstudanteSerializer
from .permissions import IsAuthenticatedAndUser
import datetime

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
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')  
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
    estudantes = Estudante.objects.filter(user=request.user)
    context_dict['estudantes'] = estudantes
    return render(request, 'home.html', context_dict)

@login_required(login_url='index')
@profile_user
def edit_student(request, context_dict, id=None):
    try:
        estudante = get_object_or_404(Estudante, pk=id) if id else None
        new = False
    except Exception as e:
        return render(request, 'error-page.html', {'title': 'Not Found 404',
                                                   'code': '404',
                                                   'message': 'Essa página não existe!'})
    if request.method == 'POST':
        form_estudante = RegisterStudentForm(request.POST)
        if form_estudante.is_valid():
            if not estudante:
                estudante = Estudante()
                new = True


            estudante.nome = form_estudante.cleaned_data['nome']
            estudante.email = form_estudante.cleaned_data['email']
            estudante.telefone = form_estudante.cleaned_data['telefone']
            estudante.endereco = form_estudante.cleaned_data['endereco']


            ### CONVERTER DATA
            data_nascimento = form_estudante.cleaned_data['data_nascimento']
            ano, mes, dia = data_nascimento.split('-')
            date_format = datetime.datetime(int(ano), int(mes), int(dia))
            estudante.data_nascimento = date_format

            estudante.data_matricula = datetime.datetime.now()

            estudante.user = request.user

            estudante.save()

            messages.success(request, 'Matrícula editada com sucesso!' if not new else 'Matrícula cadastrada com sucesso!')
            redirect_url = reverse('home', args=[])
            return HttpResponseRedirect(redirect_url)

        else:
            messages.error(request, 'Erro no formulário!')
    else:
        if estudante:
            form_estudante = RegisterStudentForm(estudante=estudante)
            if estudante.user != request.user:
                return render(request, 'error-page.html', {'title': 'Forbidden 403',
                                                           'code': '403',
                                                           'message': 'Você não pode acessar essa página!'})
        else:
            form_estudante = RegisterStudentForm()
    context_dict['label_form'] = 'Cadastro' if new else 'Edição'
    context_dict['form'] = form_estudante
    context_dict['estudante'] = estudante
    return render(request, 'register-student.html', context_dict)

@login_required(login_url='index')
def delete_student(request):
    id = request.GET.get('id')
    try:
        colaborador = get_object_or_404(Estudante, pk=int(id))
        colaborador.delete()
        messages.success(request, 'Matrícula excluída com sucesso!')
        return JsonResponse({'result': True})
    except Exception as e:
        redirect_url = reverse('home', args=[])
        return HttpResponseRedirect(redirect_url)

# @login_required(login_url='index')
# @profile_user
# def list_students(request, context_dict):
#     return render(request, 'home.html', context_dict)


class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
    permission_classes = [IsAuthenticatedAndUser]

    def get_queryset(self):
        request = self.request
        if request.user.is_authenticated:
            return Estudante.objects.filter(user=request.user)
        return Estudante.objects.none()


def quick_logout(request):
    logout(request)
    return redirect('index')