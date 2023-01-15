from django import forms


class EmailPostForm(forms.Form):
    topic = forms.CharField(label='', max_length=25, widget=forms.TextInput(attrs={'placeholder' : 'Ваше имя'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder' : 'Ваше email'}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder' : 'текст'}))
