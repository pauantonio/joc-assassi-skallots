from django import forms
from .models import Player

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['profile_picture']

class PlayerLoginForm(forms.Form):
    code = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'inputmode': 'numeric',
            'pattern': '[0-9]*'
            })
        )
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
