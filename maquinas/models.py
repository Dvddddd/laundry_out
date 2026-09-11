from django.db import models


class Maquina(models.Model):
    codigo = models.CharField('Código', max_length=50, unique=True)
    nome = models.CharField('Nome', max_length=100, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Máquina de lavar'
        verbose_name_plural = 'Máquinas de lavar'

    def __str__(self):
        return f'{self.codigo} - {self.nome}'
