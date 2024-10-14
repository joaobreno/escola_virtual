from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label='Email Address'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label='Email Address'
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Validação para garantir que o email seja único
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("O email já está cadastrado.")
        return email

    # Validação extra de senha pode ser feita aqui, se necessário
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")

        return password2
    


class RegisterStudentForm(forms.Form):

    nome = forms.CharField(
        label='Nome',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Nome (Apelido)"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'type': "text", 'class': "form-control",  'placeholder': "E-mail"}),
        required=True,
        max_length=200
    )

    data_nascimento = forms.CharField(
        widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}),
        required=True
    )

    endereco = forms.CharField(
        label='Endereço',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Endereço Completo"})
    )

    telefone = forms.CharField(
        label='Telefone',
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Telefone", 'oninput': "mascaraTelefone(this)"})
    )


    def __init__(self, *args, **kwargs):
        estudante = kwargs.pop('estudante', None)
        super(RegisterStudentForm, self).__init__(*args, **kwargs)

        if estudante:
            self.fields['nome'].initial = estudante.nome
            self.fields['email'].initial = estudante.email
            self.fields['data_nascimento'].initial = estudante.data_nascimento.strftime("%Y-%m-%d")
            self.fields['endereco'].initial = estudante.endereco
            self.fields['telefone'].initial = estudante.telefone
