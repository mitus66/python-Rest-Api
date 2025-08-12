from django import forms
from .models import Author, Quote
from django.contrib.auth.forms import UserCreationForm  # Для реєстрації користувачів


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'born_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Month DD, YYYY'}),
            'born_location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class QuoteForm(forms.ModelForm):
    # Використовуємо ModelChoiceField для вибору автора
    author = forms.ModelChoiceField(queryset=Author.objects.all().order_by('fullname'), empty_label="Оберіть автора",
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
        widgets = {
            'quote': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tag1,tag2,tag3'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)  # Додаємо email до форми реєстрації
