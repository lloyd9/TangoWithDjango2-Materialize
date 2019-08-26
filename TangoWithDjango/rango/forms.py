from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name:")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    is_liked = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)

    class Meta:
        model = Category 
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text='Please enter the title of the page:')
    url = forms.URLField(max_length=200,
                         help_text='Please enter the URL of the page:')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # Modern browsers checks the correct URL format, this method is only for older browsers
    # Override clean for URL checking
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url isn't empty and doesn't start with http://
        if url and not url.startswith('http://'):
            # Prepend http://
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)
        

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        exclude = ('user',)