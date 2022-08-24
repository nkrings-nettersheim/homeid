from django import forms


class HomeidForm(forms.Form):
    homeid = forms.CharField(
        widget=forms.TextInput(
            attrs={}
        ),
        min_length=7,
        max_length=7,
        required=True
    )

