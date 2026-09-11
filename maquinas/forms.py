from django import forms

from .models import Maquina


class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ('codigo', 'nome')
        error_messages = {
            'codigo': {
                'unique': 'Já existe uma máquina com este código.',
            },
            'nome': {
                'unique': 'Já existe uma máquina com este nome.',
            },
        }
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: ML-001',
                'maxlength': 50,
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Máquina principal',
                'maxlength': 100,
            }),
        }
