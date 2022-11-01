from modeltranslation.translator import register, TranslationOptions

from .models import Author, Category, Post, PostCategory, Comment


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('author', 'categoryType', 'text', 'dateCreation', 'title', 'rating', )


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('authorUser', 'ratingAuthor', )


@register(PostCategory)
class PostCategoryTranslationOptions(TranslationOptions):
    fields = ('post', 'cat', )


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('commentPost', 'commentUser', 'text', 'dateCreation', 'rating', )