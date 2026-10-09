from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class FormularioLogin(AuthenticationForm):
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário',
            'autofocus': True,
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
            'autocomplete': 'current-password',
        }),
    )


class FormularioCadastro(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'username',
            'autofocus': True,
        })
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].label = 'Confirmar senha'
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'new-password',
        })


class FormularioEdicaoUsuario(forms.ModelForm):
    password1 = forms.CharField(
        label='Nova senha',
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
    )
    password2 = forms.CharField(
        label='Confirmar nova senha',
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = User
        fields = ('username',)
        labels = {'username': 'Nome de usuário'}
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'username',
                'autofocus': True,
            }),
        }

    def clean(self):
        dados = super().clean()
        password1 = dados.get('password1')
        password2 = dados.get('password2')

        if password1 or password2:
            if not password1:
                self.add_error('password1', 'Informe a nova senha.')
            elif not password2:
                self.add_error('password2', 'Confirme a nova senha.')
            elif password1 != password2:
                self.add_error('password2', 'As duas senhas não coincidem.')
            else:
                validate_password(password1, self.instance)

        return dados

    def save(self, commit=True):
        usuario = super().save(commit=False)
        nova_senha = self.cleaned_data.get('password1')

        if nova_senha:
            usuario.set_password(nova_senha)

        if commit:
            usuario.save()

        return usuario

    @property
    def senha_alterada(self):
        return bool(self.cleaned_data.get('password1'))
