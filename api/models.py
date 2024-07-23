from django.db import models
from django.utils import timezone
from django.utils.formats import date_format

class Rating(models.Model):
    RATING_CHOICES = (
        ('0', 'Poor'),
        ('1', 'Good'),
        ('2', 'Excellent'),
    )
    
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Rating: {self.get_rating_display()} ({self.created_at})"


class Feedback(models.Model):
    experience = models.CharField(max_length=100)
    conflict_resolution_effectiveness = models.CharField(max_length=100)
    information_quality = models.CharField(max_length=100)
    community_service_effectiveness = models.CharField(max_length=100)
    suggestions = models.TextField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        local_time = timezone.localtime(self.created_at)
        return date_format(local_time, format='SHORT_DATETIME_FORMAT', use_l10n=True)