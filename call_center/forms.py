from datetime import datetime as dt
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
                                 initial=dt.date(dt.now()),)
                                 # required=False)
    date_finish = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                  label='Дата окончания',
                                  initial=dt.date(dt.now()),)
                                  # required=False)
    incoming_calls = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=CALL_CHOICES,
                                       initial=CALL_CHOICES[0],
                                       label='',)
                                       # required=False)


class CommentForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput, required=False)

    class Meta:
        model = Comment
        fields = ['status', 'title']
