from django.db import models
import uuid

from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(default='default.jpg')
    demo_link = models.CharField(max_length=2000, blank=True)
    source_link = models.CharField(max_length=2000, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, unique=True)

    class Meta:
        ordering = ['-vote_ratio', 'vote_total', 'title']
    
    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        all_reviewers = self.review_set.all().values_list('owner__id', flat=True)
        return all_reviewers


    @property
    def refresh_votes(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()
        ratio = (up_votes / total_votes) * 100
        self.vote_ratio = ratio
        self.vote_total = total_votes
        self.save()




class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner', 'project']]
    
    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, unique=True)
    
    def __str__(self):
        return self.name

