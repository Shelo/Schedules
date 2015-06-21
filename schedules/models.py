from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import util
import uuid

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="owner")
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    short_description = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + "_" + str(uuid.uuid1()).split("-")[0]
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    create_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        unique_together = ['user', 'project']

    def __str__(self):
        return "%s @ %s" % (self.user, self.project.name)


class OccupiedBlock(models.Model):
    membership = models.ForeignKey(Membership)
    day = models.IntegerField()
    block = models.IntegerField()

    def __str__(self):
        return "%s: %s - %s" % (self.membership, util.number_to_day(self.day), self.block)
