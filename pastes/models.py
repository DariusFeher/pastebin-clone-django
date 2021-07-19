from datetime import datetime

import pytz
from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinLengthValidator

# Create your models here.

class PastebinClone(models.Model):
	title = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
	body = models.TextField(default="Pastebin text...", validators=[MinLengthValidator(3)])
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse('detail', kwargs={'pk' : self.pk})
	
	def get_delete_url(self):
		return reverse('delete', kwargs={'pk' : self.pk})

	def save(self, *args, **kwargs):
		super(PastebinClone, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ['-updated']
	
