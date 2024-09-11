from django.db import models

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
    party = models.CharField(max_length=255)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=255)
    voter_email = models.EmailField(unique=True)
    voter_gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    voter_province = models.CharField(max_length=50, choices=[('Kigali', 'Kigali'), ('North', 'North'), ('East', 'East'), ('West', 'West'), ('South', 'South')])
    voter_phone = models.CharField(max_length=15)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter_email', 'candidate')

        

