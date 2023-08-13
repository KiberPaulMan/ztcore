from django import forms
from .models import Comment


class DateForm(forms.Form):
    CALL_CHOICES = (
        ('all_calls', 'Все звонки'),
        ('answered_calls', 'Только отвеченные звонки'),
        ('unanswered_calls', 'Только неотвеченные звонки'),
    )
    date_start = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                 label='Дата начала',
                                 required=True)
    date_finish = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                  label='Дата окончания',
                                  required=True)
    incoming_calls = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=CALL_CHOICES,
                                       initial=CALL_CHOICES[0],
                                       label='')


class CommentForm(forms.ModelForm):
    class Neta:
        model = Comment
        fields = ['status', 'title']