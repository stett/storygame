from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from braces.views import LoginRequiredMixin
from stories.models import Story, StoryAuthor, StoryChunk
from stories.forms import StoryChunkForm


@login_required
def dash(request):
    context = {
        'stories': Story.objects.filter(authors__user=request.user),
        'chunks': StoryChunk.objects.filter(user=request.user, committed=False),
    }
    return render(request, 'dash.html', context)


class StoryView(DetailView):
    template_name = 'story.html'
    model = Story


class StoryChunkEditMixin(LoginRequiredMixin):
    template_name = 'chunk.html'
    model = StoryChunk

    def dispatch(self, request, story_pk, *args, **kwargs):
        self.story = Story.objects.get(pk=story_pk)
        return super(StoryChunkEditMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        self.object = super(StoryChunkEditMixin, self).get_object()
        if self.object.committed:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context = super(StoryChunkEditMixin, self).get_context_data(**kwargs)
        context.update({'story': self.story})
        return context

    def get_success_url(self):
        if self.object.committed:
            return reverse('dash')
        else:
            return reverse('chunk', args=[self.story.pk, self.object.pk])


class StoryChunkCreateView(StoryChunkEditMixin, CreateView):
    form_class = StoryChunkForm

    def get_initial(self):
        return {
            'story': self.story,
            'user': self.request.user,
        }


class StoryChunkUpdateView(StoryChunkEditMixin, UpdateView):
    form_class = StoryChunkForm
