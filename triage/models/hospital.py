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
    city = models.CharField(
        max_length=50,
        verbose_name='城市',
        null=True,
        blank=True
    )

    district = models.CharField(
        max_length=50,
        verbose_name='区',
        null=True,
        blank=True
    )

    HOSPITAL_LEVELS = [
        ('A', '三甲医院'),
        ('B', '三级医院'),
        ('C', '二级医院'),
        ('D', '一级医院'),
        ('E', '未分级')
    ]

    level = models.CharField(
        max_length=10,
        choices=HOSPITAL_LEVELS,
        verbose_name='医院等级',
        null=True,
        blank=True
    )
    # city 城市
    # district 区
    # level 医院等级：三甲医院、三级医院、二级医院、一级医院、未分级

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '医院'
        verbose_name_plural = '医院'
        ordering = ['name']