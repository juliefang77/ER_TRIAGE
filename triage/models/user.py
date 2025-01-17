from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class HospitalUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        verbose_name='医院用户名称',
        null=True,
        blank=True
    )
    hospital = models.ForeignKey(
        'Hospital',
        on_delete=models.PROTECT,
        related_name='users',
        verbose_name='所属医院',
        null=True,
        blank=True
    )

# HospitalUser Table Relations:
# - Inherits from AbstractUser
# - Links to Hospital (ForeignKey)
# - Has many Patients (reverse relation)
# - Has many MedicalStaff (reverse relation)
# - Has many TriageRecords (reverse relation)

# Fields:
# 1. id | 唯一标识 | UUIDField (primary key)
# 2. hospital | 所属医院 | ForeignKey (Hospital)
# 3. username | 用户名 | CharField (from AbstractUser)
# 4. password | 密码 | CharField (from AbstractUser)
# 5. email | 邮箱 | EmailField (from AbstractUser)
# 6. first_name | 名 | CharField (from AbstractUser)
# 7. last_name | 姓 | CharField (from AbstractUser)
# 8. is_staff | 是否职员 | BooleanField (from AbstractUser)
# 9. is_active | 是否激活 | BooleanField (from AbstractUser)
# 10. date_joined | 加入日期 | DateTimeField (from AbstractUser)