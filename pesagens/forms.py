from django import forms

from .models import Pesagem


class CartoesSelecao(forms.RadioSelect):
    template_name = 'pesagens/cartoes.html'
    option_template_name = 'pesagens/opcao.html'

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        opcao = super().create_option(name, value, label, selected, index, subindex, attrs)
        imagem = getattr(getattr(value, 'instance', None), 'imagem', None)
        if imagem:
            opcao['imagem_url'] = imagem.url
        return opcao


class PesagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in ('maquina', 'uniforme'):
            self.fields[campo].empty_label = None

    class Meta:
        model = Pesagem
        fields = ('maquina', 'uniforme', 'peso')
        widgets = {
            'maquina': CartoesSelecao,
            'uniforme': CartoesSelecao,
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.001',
                'step': '0.001',
                'data-peso': '',
            }),
        }
