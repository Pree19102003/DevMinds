from django.contrib import admin
from .models import Profile, Resource, Tag, Rating, Comment

admin.site.register(Profile)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Comment)
