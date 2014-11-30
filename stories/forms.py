from django import forms
from stories.models import StoryChunk


class StoryChunkForm(forms.ModelForm):
    class Meta:
        model = StoryChunk
        widgets = {
            'story': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            #'committed': forms.HiddenInput(),
        }
