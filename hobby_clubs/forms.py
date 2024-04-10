from django import forms
from .models import Club, Review, Rating

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['club_name','address','activity','website']
        labels = {'club_name':'','address':'','activity':'','website':''}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['my_review']
        labels = {'my_review':''}
        widgets = {'my_review': forms.Textarea(attrs={'cols': 80})}


class RatingForm(forms.Form):
    rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)

