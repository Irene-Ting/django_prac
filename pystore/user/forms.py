from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.Form):
    product_name = forms.CharField(max_length=20)
    description = forms.CharField(max_length=255, required=False, widget=forms.Textarea())
    price = forms.IntegerField()
    inventory = forms.IntegerField()


class CommentForm(forms.Form):
    content = forms.CharField(max_length=255, widget=forms.Textarea())


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user