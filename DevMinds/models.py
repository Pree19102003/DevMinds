from django.db import models
from django.contrib.auth.models import User

# ---------------- USER PROFILE ----------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.user.username


# ---------------- TAGS ----------------
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ---------------- RESOURCE ----------------
class Resource(models.Model):
    PRIVACY_CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/')
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---------------- RATING ----------------
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    stars = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.stars}"


# ---------------- COMMENT ----------------
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
