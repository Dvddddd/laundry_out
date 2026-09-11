import json

from django.test import TestCase
from django.urls import reverse

from .models import Maquina


class MaquinaTests(TestCase):
    def test_pagina_e_publica_e_nao_exibe_coluna_id(self):
        Maquina.objects.create(codigo='ML-001', nome='Máquina Principal')

        response = self.client.get(reverse('maquinas:lista'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Máquinas de Lavar')
        self.assertContains(response, 'ML-001')
        self.assertNotContains(response, '<th scope="col">ID</th>', html=True)

    def test_cria_maquina(self):
        response = self.client.post(reverse('maquinas:lista'), {
            'codigo': 'ML-002',
            'nome': 'Máquina Dois',
        })

        self.assertRedirects(response, reverse('maquinas:lista'))
        self.assertTrue(Maquina.objects.filter(
            codigo='ML-002',
            nome='Máquina Dois',
        ).exists())

    def test_codigo_e_nome_devem_ser_unicos(self):
        Maquina.objects.create(codigo='ML-001', nome='Máquina Principal')

        response = self.client.post(reverse('maquinas:lista'), {
            'codigo': 'ML-001',
            'nome': 'Máquina Principal',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['abrir_formulario'])
        self.assertFormError(response.context['form'], 'codigo', 'Já existe uma máquina com este código.')
        self.assertFormError(response.context['form'], 'nome', 'Já existe uma máquina com este nome.')

    def test_atualiza_maquina(self):
        maquina = Maquina.objects.create(codigo='ML-001', nome='Máquina Principal')

        response = self.client.post(
            reverse('maquinas:atualizar', args=[maquina.pk]),
            data=json.dumps({'codigo': 'ML-010', 'nome': 'Máquina Atualizada'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        maquina.refresh_from_db()
        self.assertEqual(maquina.codigo, 'ML-010')
        self.assertEqual(maquina.nome, 'Máquina Atualizada')

    def test_rejeita_atualizacao_com_json_invalido(self):
        maquina = Maquina.objects.create(codigo='ML-001', nome='Máquina Principal')

        response = self.client.post(
            reverse('maquinas:atualizar', args=[maquina.pk]),
            data='{invalido',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'erro': 'Dados inválidos.'})

    def test_exclui_maquina(self):
        maquina = Maquina.objects.create(codigo='ML-001', nome='Máquina Principal')

        response = self.client.post(reverse('maquinas:excluir', args=[maquina.pk]))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Maquina.objects.filter(pk=maquina.pk).exists())

    def test_atualizar_e_excluir_nao_aceitam_get(self):
        maquina = Maquina.objects.create(codigo='ML-001', nome='Máquina Principal')

        atualizar = self.client.get(reverse('maquinas:atualizar', args=[maquina.pk]))
        excluir = self.client.get(reverse('maquinas:excluir', args=[maquina.pk]))

        self.assertEqual(atualizar.status_code, 405)
        self.assertEqual(excluir.status_code, 405)
