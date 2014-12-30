from django import forms
from stories.models import StoryChunk


class StoryChunkForm(forms.ModelForm):
    class Meta:
        model = StoryChunk
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': "Write the body of your story chunk here!"}),
            'lead_in': forms.Textarea(attrs={'placeholder': "Write a lead-in for the next player here!"}),
            'story': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            #'committed': forms.HiddenInput(),
        }
