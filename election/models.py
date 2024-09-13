from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable


class Election(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    email = models.EmailField()
    image = models.ImageField(upload_to='contestants_images/', blank=False, null=False) 
    class Meta:
        unique_together = ('email', 'election')

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=255)
    voter_email = models.EmailField()
    voter_phone = models.CharField(max_length=255)
    voter_gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    voter_province = models.CharField(max_length=50, choices=[('Kigali', 'Kigali'), ('North', 'North'), ('East', 'East'), ('West', 'West'), ('South', 'South')])
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter_email', 'election')


class Auca_User(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 100)
    timestamp = models.DateTimeField(auto_now_add = True)

    def set_password(self, input_password):
        self.password = make_password(input_password)
        self.save()

    def __str__(self):
        return self.name

