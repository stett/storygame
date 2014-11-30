from django.contrib import admin
from stories.models import Story, StoryAuthor, StoryChunk

admin.site.register(Story)
admin.site.register(StoryAuthor)
admin.site.register(StoryChunk)
