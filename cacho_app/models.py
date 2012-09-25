from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

	# connects the User model to this model (UserProfile)
	user = models.OneToOneField(User)

	score = models.IntegerField(editable=False)


