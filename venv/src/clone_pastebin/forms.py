from django import forms
from django.core.validators import MinLengthValidator

from .models import PastebinClone


class PastebinForm(forms.ModelForm):
    class Meta:
        model = PastebinClone
        title = forms.CharField()
        body = forms.CharField(widget=forms.Textarea)
        fields = {
            'title': title,
            'body': body
        }

    def clean(self):
      super(PastebinForm, self).clean()

      title = self.cleaned_data.get('title')
      body = self.cleaned_data.get('body')

      if title and len(title) < 3:
         self._errors['title'] = self.error_class(['A minimum of 3 characters is required'])

      if body and len(body) < 8:
         self._errors['body'] = self.error_class(['Body length should not be less than 3 characters'])

      return self.cleaned_data