from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ParadaMaquinaForm
from .models import ParadaMaquina


@login_required
def lista_paradas(request):
    form = ParadaMaquinaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        parada = form.save(commit=False)
        try:
            with transaction.atomic():
                if ParadaMaquina.objects.select_for_update().filter(
                    maquina=parada.maquina,
                    retorno_em__isnull=True,
                ).exists():
                    raise IntegrityError
                parada.save()
        except IntegrityError:
            form.add_error('maquina', 'Esta máquina já está em parada.')
        else:
            messages.success(request, 'Parada registrada.')
            return redirect('paradas:lista')

    busca = request.GET.get('q', '').strip()
    registros = ParadaMaquina.objects.select_related('maquina')
    if busca:
        registros = registros.filter(
            Q(maquina__nome__icontains=busca)
            | Q(maquina__codigo__icontains=busca)
            | Q(motivo__icontains=busca)
            | Q(pessoa_acionada__icontains=busca)
        )
    pagina = Paginator(registros, 10).get_page(request.GET.get('page'))
    return render(request, 'paradas/lista.html', {
        'form': form,
        'paradas': pagina,
        'q': busca,
    })


@login_required
@require_POST
def registrar_retorno(request, pk):
    parada = get_object_or_404(ParadaMaquina, pk=pk)
    if parada.retorno_em is None:
        parada.retorno_em = timezone.now()
        parada.save(update_fields=['retorno_em'])
        messages.success(request, 'Retorno da máquina registrado.')
    return redirect('paradas:lista')


@login_required
@require_POST
def excluir_parada(request, pk):
    get_object_or_404(ParadaMaquina, pk=pk).delete()
    return HttpResponse(status=204)
