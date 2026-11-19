from django.db import models


class ParadaMaquina(models.Model):
    maquina = models.ForeignKey(
        'maquinas.Maquina',
        verbose_name='Máquina',
        on_delete=models.PROTECT,
    )
    motivo = models.TextField('Motivo da parada')
    pessoa_acionada = models.CharField('Pessoa acionada', max_length=120)
    criado_em = models.DateTimeField('Data e hora da parada', auto_now_add=True)
    retorno_em = models.DateTimeField(
        'Data e hora do retorno',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Parada de máquina'
        verbose_name_plural = 'Paradas de máquina'

    def __str__(self):
        return f'{self.maquina} - {self.criado_em:%d/%m/%Y %H:%M}'
