from django.db import models


class TipoUniforme(models.Model):
    STATUS_ATIVO = 'ativo'
    STATUS_INATIVO = 'inativo'
    STATUS_ESCOLHAS = [
        (STATUS_ATIVO, 'Ativo'),
        (STATUS_INATIVO, 'Inativo'),
    ]

    nome = models.CharField('Nome', max_length=100, unique=True)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_ESCOLHAS,
        default=STATUS_ATIVO,
    )
    ordem = models.PositiveIntegerField('Ordem', default=0)
    imagem = models.ImageField(
        'Imagem',
        upload_to='uniforme_tipos/',
        null=True,
        blank=True,
        help_text='Imagem representativa do uniforme.',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Tipo de uniforme'
        verbose_name_plural = 'Tipos de uniforme'

    def __str__(self):
        return self.nome
