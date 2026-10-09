import shutil
import tempfile
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import TipoUniforme


MEDIA_TESTE = tempfile.mkdtemp()


def imagem_teste(nome='uniforme.gif'):
    conteudo = (
        b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00'
        b'\xff\xff\xff!\xf9\x04\x01\x00\x00\x01\x00,\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    )
    return SimpleUploadedFile(nome, conteudo, content_type='image/gif')


@override_settings(MEDIA_ROOT=MEDIA_TESTE)
class TipoUniformeTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='operador',
            password='SenhaMuitoForte#2026',
        )
        self.client.force_login(self.usuario)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TESTE, ignore_errors=True)

    def test_pagina_lista_campos_do_cadastro(self):
        TipoUniforme.objects.create(
            nome='Camiseta',
            status=TipoUniforme.STATUS_ATIVO,
            ordem=2,
        )

        response = self.client.get(reverse('uniformes:lista'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tipos de Uniforme')
        self.assertContains(response, 'Camiseta')
        self.assertContains(response, 'Ordem')
        self.assertContains(response, 'Imagem')
        self.assertContains(response, 'Status')

    def test_cria_uniforme_e_salva_imagem_em_media(self):
        response = self.client.post(reverse('uniformes:lista'), {
            'nome': 'Calça',
            'status': TipoUniforme.STATUS_ATIVO,
            'imagem': imagem_teste(),
        })

        self.assertRedirects(response, reverse('uniformes:lista'))
        uniforme = TipoUniforme.objects.get(nome='Calça')
        self.assertTrue(uniforme.imagem.name.startswith('uniforme_tipos/'))
        self.assertTrue(Path(uniforme.imagem.path).exists())

    def test_nome_deve_ser_unico(self):
        TipoUniforme.objects.create(nome='Jaleco')

        response = self.client.post(reverse('uniformes:lista'), {
            'nome': 'Jaleco',
            'status': TipoUniforme.STATUS_ATIVO,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['abrir_formulario'])
        self.assertFormError(
            response.context['form'],
            'nome',
            'Já existe um uniforme com este nome.',
        )

    def test_atualiza_dados_sem_apagar_imagem_existente(self):
        uniforme = TipoUniforme.objects.create(
            nome='Camiseta',
            imagem=imagem_teste(),
        )
        imagem_anterior = uniforme.imagem.name

        response = self.client.post(
            reverse('uniformes:atualizar', args=[uniforme.pk]),
            {'nome': 'Camiseta Azul', 'status': 'inativo', 'ordem': 3},
        )

        self.assertEqual(response.status_code, 200)
        uniforme.refresh_from_db()
        self.assertEqual(uniforme.nome, 'Camiseta Azul')
        self.assertEqual(uniforme.status, 'inativo')
        self.assertEqual(uniforme.ordem, 3)
        self.assertEqual(uniforme.imagem.name, imagem_anterior)
        self.assertTrue(Path(uniforme.imagem.path).exists())

    def test_substitui_imagem_e_remove_arquivo_anterior(self):
        uniforme = TipoUniforme.objects.create(
            nome='Camiseta',
            imagem=imagem_teste('antiga.gif'),
        )
        caminho_anterior = Path(uniforme.imagem.path)

        response = self.client.post(
            reverse('uniformes:atualizar', args=[uniforme.pk]),
            {
                'nome': 'Camiseta',
                'status': 'ativo',
                'ordem': 0,
                'imagem': imagem_teste('nova.gif'),
            },
        )

        self.assertEqual(response.status_code, 200)
        uniforme.refresh_from_db()
        self.assertEqual(uniforme.imagem.name, 'uniforme_tipos/nova.gif')
        self.assertFalse(caminho_anterior.exists())
        self.assertTrue(Path(uniforme.imagem.path).exists())

    def test_rejeita_atualizacao_invalida(self):
        uniforme = TipoUniforme.objects.create(nome='Camiseta')

        response = self.client.post(
            reverse('uniformes:atualizar', args=[uniforme.pk]),
            {'nome': '', 'status': 'desconhecido', 'ordem': -1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()['erros']), {'nome', 'status', 'ordem'})

    def test_exclui_uniforme_e_arquivo(self):
        uniforme = TipoUniforme.objects.create(
            nome='Avental',
            imagem=imagem_teste('avental.gif'),
        )
        caminho = Path(uniforme.imagem.path)

        response = self.client.post(reverse('uniformes:excluir', args=[uniforme.pk]))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(TipoUniforme.objects.filter(pk=uniforme.pk).exists())
        self.assertFalse(caminho.exists())

    def test_atualizar_e_excluir_nao_aceitam_get(self):
        uniforme = TipoUniforme.objects.create(nome='Avental')

        atualizar = self.client.get(reverse('uniformes:atualizar', args=[uniforme.pk]))
        excluir = self.client.get(reverse('uniformes:excluir', args=[uniforme.pk]))

        self.assertEqual(atualizar.status_code, 405)
        self.assertEqual(excluir.status_code, 405)
