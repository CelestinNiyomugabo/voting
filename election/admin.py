from django.contrib import admin
from election.models import Election, Candidate, Vote

# Register your models here.
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Vote)


