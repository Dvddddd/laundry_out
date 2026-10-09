from django import forms

from .models import TipoUniforme


class TipoUniformeForm(forms.ModelForm):
    class Meta:
        model = TipoUniforme
        fields = ('nome', 'status', 'imagem')
        error_messages = {
            'nome': {
                'unique': 'Já existe um uniforme com este nome.',
            },
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Camiseta',
                'maxlength': 100,
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class TipoUniformeAtualizacaoForm(TipoUniformeForm):
    class Meta(TipoUniformeForm.Meta):
        fields = ('nome', 'status', 'ordem', 'imagem')
        widgets = {
            **TipoUniformeForm.Meta.widgets,
            'ordem': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'min': 0,
            }),
        }
