from django import forms

from maquinas.models import Maquina
from .models import ParadaMaquina


class ParadaMaquinaForm(forms.ModelForm):
    class Meta:
        model = ParadaMaquina
        fields = ('maquina', 'pessoa_acionada', 'motivo')
        widgets = {
            'maquina': forms.Select(attrs={'class': 'form-select'}),
            'pessoa_acionada': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        em_parada = ParadaMaquina.objects.filter(
            retorno_em__isnull=True,
        ).values('maquina_id')
        self.fields['maquina'].queryset = Maquina.objects.exclude(pk__in=em_parada)
