from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import Desk

class DeskForm(forms.Form):
    """docstring for DeskForm"""

    desks = Desk.objects.all()
    current = None

    def __init__(self, *args, **kwargs):
        worker = kwargs['worker']
        self.current = kwargs['current']
        super(DeskForm, self).__init__(*args, **{})
        self.fields['desk'].queryset = worker.desks.all()
        self.fields['desk'].initial = self.current

    desk = forms.ModelChoiceField(queryset=desks, initial=current)

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'style': 'height:30px'}))
    password = forms.CharField(widget=PasswordInput(attrs={'style': 'height:30px'}))