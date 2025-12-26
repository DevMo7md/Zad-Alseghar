from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='hadith_thumbnails/', null=True, blank=True)
    video = models.FileField(upload_to='hadith_videos/', null=True, blank=True)
    order = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    

class Pdf(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='hadith_pdfs/')
    order = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title