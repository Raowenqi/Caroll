from app01.models import UserInfo
from utils.tencent.sms import send_sms_single
from django import forms
from django.forms import ModelForm
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_redis import get_redis_connection
from utils import encrypt
import random


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """钩子"""
        mobile_phone = self.cleaned_data['mobile_phone']
        # 校验已有手机号
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已存在')
        code = random.randrange(1000, 9999)
        print(code)
        sms = send_sms_single(mobile_phone, 1822929, [code, ])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败！{}".format(sms['errmsg']))
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)

        return mobile_phone


class RegisterModelForm(forms.ModelForm):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'input', 'placeholder': '请输入用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': '请输入邮箱'}))
    mobile_phone = forms.CharField(label='手机号',
                                   widget=forms.TextInput(attrs={'class': 'input', 'placeholder': '请输入手机号'}),
                                   validators=[RegexValidator('(1[3|4|5|6|7|8|9])\d{9}',
                                                              '手机号格式错误')])  # 正则表达式校验手机号是不是数字
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': '密码长度不能小于8个字符',
                                   'max_length': '密码长度不能大于64个字符'
                               },
                               widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '请输入密码'}))
    confirm_password = forms.CharField(label='重复密码',
                                       min_length=8,
                                       max_length=64,
                                       error_messages={
                                           'min_length': '密码长度不能小于8个字符',
                                           'max_length': '密码长度不能大于64个字符'
                                       },
                                       widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': '请重新输入密码'}))

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone']

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            self.add_error('username', '用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return encrypt.md5(pwd)

    def clean_confirm_password(self):

        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']

        code = self.data.get("code")
        print(self.data, code)

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        conn = get_redis_connection()
        code2 = conn.get(mobile_phone)
        print(code2, code)
        if not code2:
            raise ValidationError('验证码失效，请重新获取')
        if code2.decode('utf8') != code:
            raise ValidationError('验证码错误')
        return mobile_phone


