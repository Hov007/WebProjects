from django import forms

class DateInput(forms.Date):
    input_type = 'date'

class ExampleForm(forms.Form):
    my_date_field = forms.DateField(widget=DateInput)