from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AutenticacaoTests(TestCase):
    senha = 'SenhaMuitoForte#2026'

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='operador',
            password=self.senha,
        )

    def test_login_com_credenciais_validas(self):
        response = self.client.post(reverse('contas:login'), {
            'username': self.usuario.username,
            'password': self.senha,
        })

        self.assertRedirects(response, reverse('maquinas:lista'))
        self.assertEqual(
            self.client.session['_auth_user_id'],
            str(self.usuario.pk),
        )

    def test_login_invalido_exibe_erro(self):
        response = self.client.post(reverse('contas:login'), {
            'username': self.usuario.username,
            'password': 'senha-incorreta',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nome de usuário ou senha inválidos.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_redireciona_para_destino_solicitado_apos_login(self):
        destino = reverse('uniformes:lista')

        response = self.client.post(
            reverse('contas:login'),
            {
                'username': self.usuario.username,
                'password': self.senha,
                'next': destino,
            },
        )

        self.assertRedirects(response, destino)

    def test_paginas_exigem_login(self):
        for url in (
            reverse('maquinas:lista'),
            reverse('uniformes:lista'),
            reverse('contas:cadastro'),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f'{reverse("contas:login")}?next={url}',
                )

    def test_usuario_comum_acessa_todas_as_abas(self):
        self.assertFalse(self.usuario.is_staff)
        self.assertFalse(self.usuario.is_superuser)
        self.client.force_login(self.usuario)

        for url in (
            reverse('maquinas:lista'),
            reverse('uniformes:lista'),
            reverse('contas:cadastro'),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_usuario_autenticado_cadastra_outro_usuario(self):
        self.client.force_login(self.usuario)

        response = self.client.post(reverse('contas:cadastro'), {
            'username': 'novo_usuario',
            'password1': self.senha,
            'password2': self.senha,
        })

        self.assertRedirects(response, reverse('contas:cadastro'))
        novo_usuario = User.objects.get(username='novo_usuario')
        self.assertTrue(novo_usuario.check_password(self.senha))
        self.assertFalse(novo_usuario.is_staff)
        self.assertFalse(novo_usuario.is_superuser)

    def test_lista_usuarios_cadastrados(self):
        outro_usuario = User.objects.create_user(
            username='segundo_usuario',
            password=self.senha,
        )
        self.client.force_login(self.usuario)

        response = self.client.get(reverse('contas:cadastro'))

        self.assertContains(response, 'Usuários Cadastrados')
        self.assertContains(response, self.usuario.username)
        self.assertContains(response, outro_usuario.username)
        self.assertContains(response, reverse('contas:editar', args=[outro_usuario.pk]))
        self.assertContains(response, reverse('contas:excluir', args=[outro_usuario.pk]))

    def test_edita_nome_sem_alterar_senha(self):
        outro_usuario = User.objects.create_user(
            username='segundo_usuario',
            password=self.senha,
        )
        self.client.force_login(self.usuario)

        response = self.client.post(
            reverse('contas:editar', args=[outro_usuario.pk]),
            {
                'username': 'usuario_atualizado',
                'password1': '',
                'password2': '',
            },
        )

        self.assertRedirects(response, reverse('contas:cadastro'))
        outro_usuario.refresh_from_db()
        self.assertEqual(outro_usuario.username, 'usuario_atualizado')
        self.assertTrue(outro_usuario.check_password(self.senha))

    def test_edita_senha_propria_sem_encerrar_sessao(self):
        nova_senha = 'OutraSenhaMuitoForte#2026'
        self.client.force_login(self.usuario)

        response = self.client.post(
            reverse('contas:editar', args=[self.usuario.pk]),
            {
                'username': self.usuario.username,
                'password1': nova_senha,
                'password2': nova_senha,
            },
        )

        self.assertRedirects(response, reverse('contas:cadastro'))
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password(nova_senha))
        self.assertEqual(
            self.client.get(reverse('maquinas:lista')).status_code,
            200,
        )

    def test_edicao_rejeita_nome_repetido(self):
        outro_usuario = User.objects.create_user(
            username='segundo_usuario',
            password=self.senha,
        )
        self.client.force_login(self.usuario)

        response = self.client.post(
            reverse('contas:editar', args=[outro_usuario.pk]),
            {
                'username': self.usuario.username,
                'password1': '',
                'password2': '',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)

    def test_exclui_outro_usuario(self):
        outro_usuario = User.objects.create_user(
            username='segundo_usuario',
            password=self.senha,
        )
        self.client.force_login(self.usuario)

        response = self.client.post(
            reverse('contas:excluir', args=[outro_usuario.pk]),
        )

        self.assertRedirects(response, reverse('contas:cadastro'))
        self.assertFalse(User.objects.filter(pk=outro_usuario.pk).exists())

    def test_nao_permite_excluir_usuario_conectado(self):
        self.client.force_login(self.usuario)

        response = self.client.post(
            reverse('contas:excluir', args=[self.usuario.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('contas:cadastro'))
        self.assertTrue(User.objects.filter(pk=self.usuario.pk).exists())
        self.assertContains(response, 'Você não pode excluir o usuário conectado.')

    def test_edicao_e_exclusao_exigem_login(self):
        editar = reverse('contas:editar', args=[self.usuario.pk])
        excluir = reverse('contas:excluir', args=[self.usuario.pk])

        self.assertRedirects(
            self.client.get(editar),
            f'{reverse("contas:login")}?next={editar}',
        )
        self.assertRedirects(
            self.client.post(excluir),
            f'{reverse("contas:login")}?next={excluir}',
        )

    def test_exclusao_nao_aceita_get(self):
        outro_usuario = User.objects.create_user(
            username='segundo_usuario',
            password=self.senha,
        )
        self.client.force_login(self.usuario)

        response = self.client.get(
            reverse('contas:excluir', args=[outro_usuario.pk]),
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(User.objects.filter(pk=outro_usuario.pk).exists())

    def test_cadastro_rejeita_usuario_repetido(self):
        self.client.force_login(self.usuario)

        response = self.client.post(reverse('contas:cadastro'), {
            'username': self.usuario.username,
            'password1': self.senha,
            'password2': self.senha,
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'username',
            'Um usuário com este nome de usuário já existe.',
        )

    def test_logout_aceita_somente_post(self):
        self.client.force_login(self.usuario)

        response_get = self.client.get(reverse('contas:logout'))
        response_post = self.client.post(reverse('contas:logout'))

        self.assertEqual(response_get.status_code, 405)
        self.assertRedirects(response_post, reverse('contas:login'))
        self.assertNotIn('_auth_user_id', self.client.session)
