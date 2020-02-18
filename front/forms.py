from django import forms

from shelves.models import Review


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(max_length=50)


class SignupForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)


class SearchForm(forms.Form):
    term = forms.CharField(label="Term", max_length=100)


class SubscribeForm(forms.Form):
    isbn = forms.CharField(label="isbn", max_length=100)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["book", "description", "star"]
