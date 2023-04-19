from django import forms
from django.forms import ModelForm
from .models import FlashCard


class FlashCardAdder(ModelForm):
    class Meta:
        model = FlashCard
        fields = ('front', 'back', 'mnemo')

        labels = {
            'front': '',
            'back': '',
            'mnemo': '',
        }

        widgets = {
            'front': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Przód karty'}),
            'back': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Tył karty'}),
            'mnemo': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Zdanie ułatwiające zapamiętanie'}),
        }


# class FlashCardForm(forms.ModelForm):
#     back = forms.CharField(
#         label='',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Tłumaczenie',
#             'autocomplete': 'off'}
#         ))
#
#     class Meta:
#         model = FlashCard
#         fields = ('back',)

class FlashCardForm(forms.Form):
    back = forms.CharField(label='', max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Enter answer'}))





