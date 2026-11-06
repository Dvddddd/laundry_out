from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from maquinas.models import Maquina
from uniformes.models import TipoUniforme

from .models import Pesagem


class PesagemTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_user(username='operador'))
        self.maquina = Maquina.objects.create(codigo='MAQ1', nome='Máquina 1')
        self.uniforme = TipoUniforme.objects.create(nome='Bota')
        self.dados = {
            'maquina': self.maquina.pk,
            'uniforme': self.uniforme.pk,
            'peso': '1.250',
        }
        self.lista = reverse('pesagens:lista')

    def test_cadastra_edita_e_exclui_pesagem(self):
        self.assertRedirects(self.client.post(self.lista, self.dados), self.lista)
        pesagem = Pesagem.objects.get()
        self.assertEqual(pesagem.maquina, self.maquina)
        self.assertEqual(pesagem.uniforme, self.uniforme)
        self.assertEqual(pesagem.peso, Decimal('1.250'))

        edicao = reverse('pesagens:editar', args=[pesagem.pk])
        response = self.client.get(edicao)
        self.assertContains(response, 'Editar pesagem')
        self.assertContains(response, 'checked', count=2)
        self.assertRedirects(
            self.client.post(edicao, {**self.dados, 'peso': '2.500'}), self.lista,
        )
        pesagem.refresh_from_db()
        self.assertEqual(pesagem.peso, Decimal('2.500'))

        exclusao = reverse('pesagens:excluir', args=[pesagem.pk])
        self.assertEqual(self.client.get(exclusao).status_code, 405)
        self.assertRedirects(self.client.post(exclusao), self.lista)
        self.assertFalse(Pesagem.objects.exists())

    def test_rejeita_peso_zero_e_selecao_ausente(self):
        response = self.client.post(self.lista, {**self.dados, 'peso': '0', 'maquina': ''})
        self.assertIn('maquina', response.context['form'].errors)
        self.assertIn('peso', response.context['form'].errors)
        self.assertFalse(Pesagem.objects.exists())

    def test_remocao_do_cadastro_preserva_a_pesagem(self):
        pesagem = Pesagem.objects.create(
            maquina=self.maquina, uniforme=self.uniforme, peso=Decimal('1.250'),
        )
        self.maquina.delete()
        self.uniforme.delete()

        pesagem.refresh_from_db()
        self.assertIsNone(pesagem.maquina)
        self.assertIsNone(pesagem.uniforme)
        self.assertEqual(pesagem.peso, Decimal('1.250'))
