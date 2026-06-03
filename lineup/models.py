from django.db import models
from django.conf import settings


class Session(models.Model):
    """Represents a RNB session"""
    name = models.CharField(max_length=100, default="Main Room")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Participant(models.Model):
    """Represents a participant in the queue"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='participants')
    screen_name = models.CharField(max_length=100)
    position = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['position']
        unique_together = ('session', 'screen_name')
    
    def __str__(self):
        return f"{self.screen_name} (Session: {self.session.name})"


class EventRegistration(models.Model):
    """A registration event created by Admin or Host"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_registrations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EventRegistrationEntry(models.Model):
    """A user's registration for a specific EventRegistration"""
    registration = models.ForeignKey(EventRegistration, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('registration', 'user')
        ordering = ['registered_at']

    def __str__(self):
        return f"{self.user.username} → {self.registration.title}"
