from django.db import models


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
