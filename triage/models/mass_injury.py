from django.db import models

class MassInjury(models.Model):
    """群伤"""
    MASS_TYPE_CHOICES = [
        ('FIGHT', '打架'),
        ('TRAFFIC', '车祸'),
        ('FLOOD', '洪水'),
        ('FIRE', '火灾'),
        ('EARTHQUAKE', '地震'),
        ('MUDSLIDE', '泥石流'),
        ('TYPHOON', '台风'),
        ('EXPLOSION', '爆炸'),
        ('PUBLIC_HEALTH', '公共卫生'),
        ('FOOD_POISON', '食物中毒'),
        ('OTHER', '其他'),
    ]

    hospital = models.ForeignKey(
        'Hospital',
        on_delete=models.PROTECT,
        related_name='mass_injuries',  # Access mass injuries from hospital
        verbose_name='所属医院',
        null=True,
        blank=True
    )

    mass_time = models.DateTimeField(
        verbose_name='事件时间',
        blank=True, 
        null=True
    )
    
    mass_type = models.CharField(
        verbose_name='事件类型',
        max_length=20,
        choices=MASS_TYPE_CHOICES,
        blank=True, 
        null=True
    )
    
    mass_name = models.CharField(
        verbose_name='事件名称',
        max_length=200,  # Adjust length as needed
        blank=True,     # Required field
        null=True
    )
    
    mass_number = models.IntegerField(
        verbose_name='群伤人数',
        blank=True,     # Required field
        null=True
    )
    
    mass_notes = models.TextField(
        verbose_name='补充说明',
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = '群伤'
        verbose_name_plural = '群伤'
        ordering = ['-mass_time']  # Most recent first

    def __str__(self):
        return f"{self.mass_name} - {self.mass_number}人"