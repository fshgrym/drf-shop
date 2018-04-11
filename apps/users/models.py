from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    '''
    用户
    '''
    name = models.CharField(max_length=30, null=True, blank=True,
                            verbose_name='姓名',help_text='姓名')  # blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月',help_text='出生年月')
    mobile = models.CharField(max_length=11, verbose_name='手机号码',null=True,blank=True,help_text='手机号码')
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default='female',
                              verbose_name='性别',help_text='性别')
    email = models.CharField(max_length=100, null=True, blank=True,
                             verbose_name='邮箱',help_text='邮箱')  # blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填

    class Meta:
        verbose_name_plural = verbose_name = '用户'

    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    '''
    短信验证码
    '''

    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name_plural = verbose_name = '短信验证码'

    def __str__(self):
        return self.code
