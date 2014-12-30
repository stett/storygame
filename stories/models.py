from django.db import models
from django.conf import settings
from random import shuffle
from django.contrib.auth.models import User


class StoryManager(models.Manager):
    def get_top(self, user):
        """
        Return the top story that "user" should work on.
        If there is none, start a new one?
        """
        if not user.is_authenticated():
            return None
        author = StoryAuthor.objects.filter(
            user=user,
            active=True,
            story__completed=False).first()
        if author:
            return author.story
        else:
            story = Story()
            story.save()

            # Add all users as authors to this new story! Woo!
            for user in User.objects.all():
                author = StoryAuthor(story=story, user=user)
                author.save()

            # Activate this author as the first author of this story
            author = StoryAuthor.objects.get(story=story, user=user)
            author.activate()

            return story


class Story(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    size = models.PositiveIntegerField(default=5, max_length=5)
    completed = models.BooleanField(default=False)
    objects = StoryManager()

    def complete(self):
        self.completed = True
        self.save()

    def get_completion(self):
        chunks = len(self.chunks.filter(committed=True))
        return 100 * chunks / self.size

    def get_active_author(self):
        try:
            return self.authors.get(active=True)
        except:
            return False

    def get_last_chunk(self):
        return StoryChunk.objects.filter(story=self, committed=True).last()

    def get_current_chunk(self):
        return StoryChunk.objects.filter(story=self, committed=False).last()

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

    def save(self):
        super(StoryChunk, self).save()
        if len(self.story.chunks.filter(committed=True)) >= self.story.size:
            self.story.complete()


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

    #def __str__(self):
    #    return self.user

    class Meta():
        ordering = ['order']
