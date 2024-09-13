# forms.py
from django import forms

class VoteForm(forms.Form):
    candidate_id = forms.IntegerField(widget=forms.HiddenInput())
    voter_name = forms.CharField(label="Your name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    voter_email = forms.EmailField(label="Your email", widget=forms.EmailInput(attrs={'class': 'form-control', 'id':'voter_email'}))
    voter_phone = forms.CharField(label="Phone number", widget=forms.TextInput(attrs={'class': 'form-control', 'id':'voter_email'}))
    voter_gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.Select(attrs={'class': 'form-control'}))
    voter_province = forms.ChoiceField(choices=[
        ('Kigali', 'Kigali'),
        ('North', 'North'),
        ('East', 'East'),
        ('West', 'West'),
        ('South', 'South')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    otp_code = forms.CharField(
        label="OTP Code",
        max_length=6, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'otp_code_field', 'style': 'display:none;'})
    )

