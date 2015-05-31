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
            # TODO: Maybe this algorithm oughta be complexified a bit some time...
            for u in User.objects.all():
                story.add_author(u)

            # Shuffle up them authors
            story.shuffle_authors()

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

    def get_first_author(self):
        return self.authors.filter(previous=None).first()

    def get_last_author(self):
        return self.authors.filter(next=None).last()

    def add_author(self, user):

        # If the author already exists, skip
        if user in self.authors.all():
            return

        # Make a new story author
        last_author = self.get_last_author()
        author = StoryAuthor(story=self, user=user, next=self.get_first_author())
        author.save()
        if last_author:
            last_author.next = author
            last_author.save()

        # Shuffle up the authors
        #self.shuffle_authors()

    def shuffle_authors(self):

        authors = StoryAuthor.objects.filter(story=self).order_by('?')
        prev_author = None
        for author in authors:
            author.next = None
            author.save()
            if prev_author:
                prev_author.next = author
                prev_author.save()
            prev_author = author

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

        # If it's the end of the story, mark it as complete
        if len(self.story.chunks.filter(committed=True)) >= self.story.size:
            self.story.complete()

        # If it's not the end of the story but it is committed,
        # advance the active user
        elif self.committed:
            author = StoryAuthor.objects.get(story=self.story, user=self.user)
            author.next.activate()


class StoryAuthor(models.Model):
    story = models.ForeignKey(Story, related_name="authors")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    next = models.OneToOneField(
        'StoryAuthor', related_name="previous", null=True, blank=True)
    active = models.BooleanField(default=False)

    def deactivate(self):
        self.active = False
        self.save()

    def activate(self):

        print(str(self.user))

        # Deactivate other active authors on this one's story
        for author in self.story.authors.filter(active=True):
            author.deactivate()

        # Activate this one
        self.active = True
        self.save()

    def __str__(self):
        return str(self.user)

    #class Meta():
    #    ordering = ['order']
