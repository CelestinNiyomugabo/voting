from django.contrib import admin
from election.models import Election, Candidate, Vote, Auca_User

# Register your models here.
admin.site.register(Auca_User)
admin.site.register(Election)
admin.site.register(Candidate)
admin.site.register(Vote)



