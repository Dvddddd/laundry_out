from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import TipoUniformeAtualizacaoForm, TipoUniformeForm
from .models import TipoUniforme


@require_http_methods(['GET', 'POST'])
def lista_uniformes(request):
    form = TipoUniformeForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('uniformes:lista')

    return render(request, 'uniformes/lista.html', {
        'form': form,
        'uniformes': TipoUniforme.objects.all(),
        'status_escolhas': TipoUniforme.STATUS_ESCOLHAS,
        'abrir_formulario': request.method == 'POST',
    })


@require_POST
def atualizar_uniforme(request, pk):
    uniforme = get_object_or_404(TipoUniforme, pk=pk)
    imagem_anterior = uniforme.imagem.name if uniforme.imagem else None
    armazenamento = uniforme.imagem.storage
    form = TipoUniformeAtualizacaoForm(
        request.POST,
        request.FILES,
        instance=uniforme,
    )

    if not form.is_valid():
        erros = {
            campo: [erro['message'] for erro in lista]
            for campo, lista in form.errors.get_json_data().items()
        }
        return JsonResponse({'erros': erros}, status=400)

    uniforme = form.save()

    if (
        'imagem' in request.FILES
        and imagem_anterior
        and imagem_anterior != uniforme.imagem.name
    ):
        armazenamento.delete(imagem_anterior)

    return JsonResponse({
        'id': uniforme.pk,
        'nome': uniforme.nome,
        'status': uniforme.status,
        'status_label': uniforme.get_status_display(),
        'ordem': uniforme.ordem,
        'imagem_url': uniforme.imagem.url if uniforme.imagem else None,
    })


@require_POST
def excluir_uniforme(request, pk):
    uniforme = get_object_or_404(TipoUniforme, pk=pk)
    imagem_nome = uniforme.imagem.name if uniforme.imagem else None
    armazenamento = uniforme.imagem.storage
    uniforme.delete()

    if imagem_nome:
        armazenamento.delete(imagem_nome)

    return HttpResponse(status=204)
