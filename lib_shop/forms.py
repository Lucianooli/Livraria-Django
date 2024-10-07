from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.ModelForm):
    password_1 = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))
    password_2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}))

    class Meta:
        model = User
        fields = ['username', 'email']  # Use 'username' e 'email' corretos do modelo User
        labels = {
            'username': 'Usuário',  # Rótulo do campo 'username' alterado para 'Usuário'
            'email': 'E-mail',      # Rótulo do campo 'email' alterado para 'E-mail'
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError("As senhas não coincidem.")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Esse nome de usuário já está em uso. Por favor, escolha outro.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Esse e-mail já está em uso. Tente outro ou faça login.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_1'])  # Criptografa a senha
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome do usuário"
        self.fields['password'].label = "Senha"