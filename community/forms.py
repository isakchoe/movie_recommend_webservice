from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'rate', 'content',]

        # movie. 
        # 다른 템플릿 

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]
