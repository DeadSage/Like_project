from django import forms
from django.core import validators
from .models import Bb, Rubric
from captcha.fields import CaptchaField


class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара',
                            validators=[validators.RegexValidator(regex='^.{3,}$')],
                            error_messages={'invalid': 'Слишком короткое название товара'})
    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрика', help_text='Категория товара',
                                    widget=forms.widgets.Select(attrs={'size': 5}))
    captcha = CaptchaField()

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')
