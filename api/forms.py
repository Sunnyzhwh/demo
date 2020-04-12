from django import forms
from api.models import User, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'dating_sex', 'dating_city', 'min_dating_age',
            'max_dating_age', 'min_distance', 'max_distance',
            'vibration', 'only_match', 'auto_play',
        ]

    def clean_max_dating_age(self):
        cleaned_data = super().clean()
        min_dating_age = cleaned_data.get('min_dating_age')
        max_dating_age = cleaned_data.get('max_dating_age')
        if min_dating_age > max_dating_age:
            raise forms.ValidationError('min_daing_age > max_dating_age')
        else:
            return max_dating_age


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'phone', 'nickname', 'sex',
            'location', 'avatar', 'birth_year',
            'birth_month', 'birth_day',
        ]
