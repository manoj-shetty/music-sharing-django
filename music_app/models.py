from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'

    ACCESS_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music_files/')
    access_type = models.CharField(max_length=10, choices=ACCESS_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    allowed_emails = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    def has_access(self, email):
        if self.access_type == MusicFile.PROTECTED:
            allowed_emails = self.allowed_emails.split(',')
            if email in allowed_emails:
                return True
            return False
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional user profile fields here

    def __str__(self):
        return self.user.username
