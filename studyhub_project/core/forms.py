from django import forms

RATING_CHOICES = [
    ("", "No rating"),
    ("1", "1 - Poor"),
    ("2", "2 - Fair"),
    ("3", "3 - Good"),
    ("4", "4 - Very good"),
    ("5", "5 - Excellent"),
]


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    rating = forms.ChoiceField(choices=RATING_CHOICES, required=False)

    def clean_message(self):
        message = self.cleaned_data["message"]
        if len(message.strip()) < 20:
            raise forms.ValidationError("Your message must be at least 20 characters long.")
        return message