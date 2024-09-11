# forms.py
from django import forms

class VoteForm(forms.Form):
    candidate_id = forms.IntegerField(widget=forms.HiddenInput())
    voter_name = forms.CharField(label="Your Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    voter_email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    voter_gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], widget=forms.Select(attrs={'class': 'form-control'}))
    voter_province = forms.ChoiceField(choices=[
        ('Kigali', 'Kigali'),
        ('North', 'North'),
        ('East', 'East'),
        ('West', 'West'),
        ('South', 'South')
    ], widget=forms.Select(attrs={'class': 'form-control'}))

