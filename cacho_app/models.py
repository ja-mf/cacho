from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class GameRoom(models.Model):

    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True)
    state = models.BooleanField(default=False) 

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("room", (self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(GameRoom, self).save(*args, **kwargs)

