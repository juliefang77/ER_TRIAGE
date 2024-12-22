from django.db import models

class MedicalStaff(models.Model):
    ROLE_CHOICES = [
        ('DOC', '医生'),
        ('NUR', '护士'),
        ('ADM', '管理员'),
    ]

    staff_id = models.CharField(max_length=10, unique=True, verbose_name='工号')
    name = models.CharField(max_length=50, verbose_name='姓名', null=True, blank=True)
    role = models.CharField(
        max_length=3, 
        choices=ROLE_CHOICES, 
        default='NUR',
        verbose_name='角色'
    )
    department = models.CharField(max_length=50, verbose_name='科室', null=True, blank=True)

    def __str__(self):
        return f"{self.name or '未知'} ({self.get_role_display()})"

    class Meta:
        verbose_name = '医护人员'
        verbose_name_plural = '医护人员'
        