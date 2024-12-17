from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    website = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.title


class iframeVideo(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()

    def save(self, *args, **kwargs):
        if "youtube.com" in self.video_url:
            self.video_url = self.add_youtube_params(self.video_url)
        super().save(*args, **kwargs)

    def add_youtube_params(self, video_url):

        if "?" in video_url:
            return video_url + "&autoplay=1&mute=1&controls=0&modestbranding=1&showinfo=0&fs=0&loop=1"
        else:
            return video_url + "?autoplay=1&mute=1&controls=0&modestbranding=1&showinfo=0&fs=0&loop=1"

    def __str__(self):
        return self.title

class adsitem(models.Model):
    title = models.CharField(max_length=200)
    ad_url = models.URLField()
    ref_url = models.URLField(default='https://default-url.com')