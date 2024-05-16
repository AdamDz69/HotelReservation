from django import forms
from .models import Reservation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control timepicker'}))
 
    class Meta:
        model = Reservation
        fields = ['name', 'start_date', 'start_time', 'end_date', 'end_time']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')