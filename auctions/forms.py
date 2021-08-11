from django import forms
from .models import  Bid, Comment, Listing, Category

choices = Category.objects.all().values_list('name','name') # 'name' from models.py-->Category-->name

choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    """Form for the image model"""

    class Meta:
        
        model = Listing
        fields = ('owner','item', 'category', 'description', 'price', 'image')

        widgets = { 
        'item': forms.TextInput(attrs={'class': 'form-control'}),     #'item': forms.TextInput(attrs={'class': 'form-control','placeholder': choice}),    ::: to see what inside choice(kind of debug :)
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'category' : forms.Select(choices=choice_list, attrs={'class' : 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'owner': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id':'owner', 'type': 'hidden'}),
        } 

class CommentForm(forms.ModelForm):  
  class Meta:
    model = Comment
    fields = ['title','body']

    widgets = {
    'title': forms.TextInput(attrs={'class': 'form-control'}), 
    'body': forms.Textarea(attrs={'class': 'form-control'}),
     }
