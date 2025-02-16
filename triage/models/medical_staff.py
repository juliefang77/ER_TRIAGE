from django.db import models

class MedicalStaff(models.Model):
    ROLE_CHOICES = [
        ('DOC', '医生'),
        ('NUR', '护士'),
        ('ADM', '管理员'),
    ]
    hospital = models.ForeignKey(
        'Hospital',
        on_delete=models.CASCADE,
        related_name='staff',
        null=True, # Nullable for now
        blank=True,
        verbose_name='所属医院'
    )

    staff_id = models.CharField(max_length=10, unique=True, verbose_name='工号', null = True, blank = True)
    name = models.CharField(max_length=50, verbose_name='姓名', null=True, blank=True)
    role = models.CharField(
        max_length=3, 
        choices=ROLE_CHOICES, 
        default='NUR',
        verbose_name='角色',
        null = True,
        blank = True
    )

    department = models.CharField(max_length=50, verbose_name='科室', null=True, blank=True)

    def __str__(self):
        return f"{self.name or '未知'} ({self.get_role_display()})"

    class Meta:
        verbose_name = '医护人员'
        verbose_name_plural = '医护人员'

# MedicalStaff Table Relations:
# - Links to HospitalUser (ForeignKey)
# - Has many TriageRecords (reverse relation)

# Fields:
# 1. id | 唯一标识 | UUIDField (primary key)
# 2. hospital | 所属医院 | ForeignKey (HospitalUser)
# 3. staff_id | 工号 | CharField (unique)
# 4. name | 姓名 | CharField
# 5. role | 角色 | CharField (choices)
# 6. department | 科室 | CharField

# Meta:
# verbose_name: 医护人员
# verbose_name_plural: 医护人员