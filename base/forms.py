from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Blog, User


class NonStrippingCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['strip'] = False
        kwargs['initial'] = ''  # Set an empty string as default value
        super(NonStrippingCharField, self).__init__(*args, **kwargs)        


class BlogForm(ModelForm):
    # content = NonStrippingCharField(label="Content", widget=forms.Textarea)

    content = NonStrippingCharField(
        label="Content", 
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'rows': 5
        })
    )

    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'description',] # 'avatar' to upload image
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'email': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'bio': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

