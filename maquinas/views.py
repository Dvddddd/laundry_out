import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import MaquinaForm
from .models import Maquina


@require_http_methods(['GET', 'POST'])
def lista_maquinas(request):
    form = MaquinaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('maquinas:lista')

    return render(request, 'maquinas/lista.html', {
        'form': form,
        'maquinas': Maquina.objects.all(),
        'abrir_formulario': request.method == 'POST',
    })


@require_POST
def atualizar_maquina(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'erro': 'Dados inválidos.'}, status=400)

    form = MaquinaForm(dados, instance=maquina)
    if not form.is_valid():
        erros = {
            campo: [erro['message'] for erro in lista]
            for campo, lista in form.errors.get_json_data().items()
        }
        return JsonResponse({'erros': erros}, status=400)

    maquina = form.save()
    return JsonResponse({
        'id': maquina.pk,
        'codigo': maquina.codigo,
        'nome': maquina.nome,
    })


@require_POST
def excluir_maquina(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    maquina.delete()
    return HttpResponse(status=204)
