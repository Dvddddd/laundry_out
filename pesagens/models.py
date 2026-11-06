from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Pesagem(models.Model):
    maquina = models.ForeignKey(
        'maquinas.Maquina',
        verbose_name='Máquina de lavar',
        null=True,
        on_delete=models.SET_NULL,
    )
    uniforme = models.ForeignKey(
        'uniformes.TipoUniforme',
        verbose_name='Tipo de uniforme',
        null=True,
        on_delete=models.SET_NULL,
    )
    peso = models.DecimalField(
        'Peso (kg)',
        max_digits=8,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
    )

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.CheckConstraint(condition=models.Q(peso__gt=0), name='pesagem_peso_positivo'),
        ]
