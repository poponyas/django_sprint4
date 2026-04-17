from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pub_date:
            self.initial['pub_date'] = self.instance.pub_date.strftime('%Y-%m-%dT%H:%M')

            
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)