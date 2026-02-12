from django import forms

class FittingRequestForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-6 py-4 bg-gray-50 border border-gray-200 rounded-full focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all placeholder-gray-400',
            'placeholder': 'Ваше имя'
        })
    )
    phone = forms.CharField(
        label='Номер телефона',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-6 py-4 bg-gray-50 border border-gray-200 rounded-full focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all placeholder-gray-400',
            'placeholder': 'Номер телефона'
        })
    )
    comment = forms.CharField(
        label='Комментарий',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-6 py-4 bg-gray-50 border border-gray-200 rounded-[2rem] focus:outline-none focus:border-black focus:ring-1 focus:ring-black transition-all placeholder-gray-400',
            'placeholder': 'Комментарий (желаемое время и т.д.)',
            'rows': 3
        })
    )
