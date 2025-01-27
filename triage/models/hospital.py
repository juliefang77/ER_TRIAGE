from django.db import models

class Hospital(models.Model):
    
    name = models.CharField(
        max_length=200,
        verbose_name='医院名称',
        null=True,
        blank=True
    )
    
    address = models.CharField(
        max_length=200,
        verbose_name='地址',
        null=True,
        blank=True
    )
    
    contact_number = models.CharField(
        max_length=20,
        verbose_name='联系电话',
        null=True,
        blank=True
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '医院'
        verbose_name_plural = '医院'
        ordering = ['name']