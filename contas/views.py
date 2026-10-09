from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import (
    FormularioCadastro,
    FormularioEdicaoUsuario,
    FormularioLogin,
)


class EntrarView(LoginView):
    authentication_form = FormularioLogin
    redirect_authenticated_user = True
    template_name = 'contas/login.html'


@login_required
@require_http_methods(['GET', 'POST'])
def cadastro(request):
    form = FormularioCadastro(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        messages.success(
            request,
            f'Usuário {usuario.username} cadastrado com sucesso.',
        )
        return redirect('contas:cadastro')

    return render(request, 'contas/cadastro.html', {
        'form': form,
        'usuarios': User.objects.order_by('username'),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = FormularioEdicaoUsuario(request.POST or None, instance=usuario)

    if request.method == 'POST' and form.is_valid():
        usuario = form.save()

        if usuario.pk == request.user.pk and form.senha_alterada:
            update_session_auth_hash(request, usuario)

        messages.success(request, 'Usuário atualizado com sucesso.')
        return redirect('contas:cadastro')

    return render(request, 'contas/editar.html', {
        'form': form,
        'usuario_editado': usuario,
    })


@login_required
@require_POST
def excluir_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    if usuario.pk == request.user.pk:
        messages.error(request, 'Você não pode excluir o usuário conectado.')
        return redirect('contas:cadastro')

    nome_usuario = usuario.username
    usuario.delete()
    messages.success(request, f'Usuário {nome_usuario} excluído com sucesso.')
    return redirect('contas:cadastro')


@login_required
@require_POST
def sair(request):
    logout(request)
    return redirect('contas:login')
