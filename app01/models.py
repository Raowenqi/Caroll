from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # 创建索引
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32,
                                    validators=[RegexValidator('(1[3|4|5|6|7|8|9])\d{9}',
                                                               '手机号格式错误')])
    password = models.CharField(verbose_name='密码', max_length=32)


class UserFile(models.Model):
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    filepath = models.CharField("文件路径", max_length=128)
