from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Plant,ChannelPost


class PlantForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={"placeholder": "Enter your Plantar plants here",
                                      "class": "form-control"}
                           ),
                           label="",
                           )

    class Meta:
        model = Plant
        exclude = ("user",)


class ChannelPostForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={"placeholder": "Enter your Channel plants here",
                                      "class": "form-control"}
                           ),
                           label="",
                           )
    class Meta:
        model = ChannelPost
        exclude = ("author",)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<small class="text-muted">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'password1'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<small class="text-muted">Passord should be at least 8 characters.<br> Don\'t use first and last name.<br> Don\'t use email.</small>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'password2'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<small class="text-muted">Required. Enter the same password as before, for verification.</small>'
