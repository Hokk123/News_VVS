from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Author, User


class ProfilForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]


class PostForm(forms.ModelForm):
    post_heading = forms.CharField(min_length=2)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'postCategory',
            'author',
            'rating'
        ]

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("post_heading")
        text = cleaned_data.get("post_text")

        if heading == text:
            raise ValidationError(
                "Заголовок не должно быть идентичен тексту статьи."
            )
        return cleaned_data