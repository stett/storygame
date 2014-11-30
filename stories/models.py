from django.db import models
from django.conf import settings
from random import shuffle


class Story(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    def get_active_author(self):
        try:
            return self.authors.get(active=True)
        except:
            return False

    def get_last_chunk(self):
        return StoryChunk.objects.filter(story=self, committed=True).last()

    def get_cat(self):
        cat = ""
        for chunk in self.chunks.all():
            cat = "%s\n\n%s\n\n%s" % (cat, chunk.body, chunk.lead_in)
        return cat

    def add_author(self, user):

        # If the author already exists, skip
        if user in self.authors:
            return

        # Make a new story author
        author = StoryAuthor(story=self)
        author.save()

        # Shuffle up the authors
        self.shuffle_authors()

    def shuffle_authors(self):

        # Randomize the order of the authors of this story
        orders = range(0, len(self.authors) - 1)
        shuffle(order)
        for author, order in zip(self.authors, orders):
            author.order = order
            author.save()

        # If the story wasn't already started,
        # set the first author as the active one
        author = self.authors.first()
        if author > 0 and not self.get_active_author():
            author.activate()

    def __str__(self):
        return self.title if self.title else "Untitled #%s" % self.pk


class StoryChunk(models.Model):
    story = models.ForeignKey(Story, related_name="chunks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    body = models.TextField()
    lead_in = models.TextField()
    committed = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)


class StoryAuthor(models.Model):
    story = models.ForeignKey(Story, related_name="authors")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.IntegerField(Story, default=0)
    active = models.BooleanField(default=False)

    def deactivate(self):
        self.active = False
        self.save()

    def activate(self):

        # Deactivate other active authors on this one's story
        for author in self.story.authors.filter(active=True):
            author.deactivate()

        # Activate this one
        self.active = True
        self.save()

    class Meta():
        ordering = ['order']
