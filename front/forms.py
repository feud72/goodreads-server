from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(max_length=50)


class SignupForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)


class UserEditForm(forms.Form):
    username = forms.EmailField(label="Email", max_length=100)
    password1 = forms.CharField(max_length=50, required=False)
    password2 = forms.CharField(max_length=50, required=False)
    nickname = forms.CharField(max_length=100, required=False)


class SearchForm(forms.Form):
    term = forms.CharField(label="Term", max_length=100)


class SubscribeForm(forms.Form):
    isbn = forms.CharField(label="isbn", max_length=100)


class ReviewForm(forms.Form):
    book = forms.CharField(label="book")
    description = forms.CharField(label="description")
    star = forms.IntegerField()
