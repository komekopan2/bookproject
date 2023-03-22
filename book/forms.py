""" from django import forms


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'text', 'thumbnail', 'category', 'user')
 """
