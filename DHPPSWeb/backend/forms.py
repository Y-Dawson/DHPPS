from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    phonenum = forms.CharField(label="手机号", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

    def format(self):
        return {u'username': self.token,
                u'password': self.content,
                u'captcha': self.captcha}
