from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import PesagemForm
from .models import Pesagem


def _renderizar_lista(request, form, editando=None):
    return render(request, 'pesagens/lista.html', {
        'form': form,
        'editando': editando,
        'pesagens': Pesagem.objects.select_related('maquina', 'uniforme'),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def lista_pesagens(request):
    form = PesagemForm(request.POST if request.method == 'POST' else None)
    if form.is_bound and form.is_valid():
        form.save()
        return redirect('pesagens:lista')

    return _renderizar_lista(request, form)


@login_required
@require_http_methods(['GET', 'POST'])
def editar_pesagem(request, pk):
    pesagem = get_object_or_404(Pesagem, pk=pk)
    form = PesagemForm(
        request.POST if request.method == 'POST' else None,
        instance=pesagem,
    )
    if form.is_bound and form.is_valid():
        form.save()
        return redirect('pesagens:lista')

    return _renderizar_lista(request, form, editando=pesagem.pk)


@login_required
@require_POST
def excluir_pesagem(request, pk):
    get_object_or_404(Pesagem, pk=pk).delete()
    return redirect('pesagens:lista')
