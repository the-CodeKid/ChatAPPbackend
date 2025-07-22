from django.db import models

class Messages(models.Model):
    room = models.CharField(max_length=64)
    username = models.CharField(max_length=64, default="Anonymous")
    text = models.TextField(blank=True)
    file_url = models.URLField(blank=True, null=True)
    file_name = models.CharField(max_length=225, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp:%H:%M:%S} | {self.username}: {self.text or self.file_name}'