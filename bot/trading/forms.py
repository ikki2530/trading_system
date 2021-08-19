from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# custom models
from .models import CryptoBase, CryptoCoin, TradingHistory, Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TradingHistoryForm(forms.ModelForm):
    print("hello from trading history form")
    class Meta:
        model = TradingHistory
        fields = "__all__"
        exclude = ['profile', 'status', 'sell_price', 'total']


class TradingHistorySearchForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        # https://stackoverflow.com/questions/7299973/django-how-to-access-current-request-user-in-modelform
        super(TradingHistorySearchForm, self).__init__(*args, **kwargs)
        if self.user.groups.filter(name="admin"):
            self.fields['profile'] = forms.ModelChoiceField(queryset=Profile.objects.all(),
                                                            widget=forms.Select(attrs={'class': 'form-control'}),
                                                            required=False)

    OPTIONS = (
        ("Open", "Open"),
        ("Close", "Close"),
    )

    TYPE_ORDER = (
        ('Buy', 'Buy'),
        ('Sell', 'Sell')
    )

    start_date = forms.DateTimeField(required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd',
                                                                    'class': 'form-control'}))
    end_date = forms.DateTimeField(required=False,
                                   widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd',
                                                                 'class': 'form-control'}))
    status = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS, required=False)

    type_order = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TYPE_ORDER, required=False)
    # coin_search = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'BTC/USDT'}))
    coin_search = forms.ModelChoiceField(queryset=CryptoCoin.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         required=False)
    base_search = forms.ModelChoiceField(queryset=CryptoBase.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         required=False)
    class Meta:
        model = TradingHistory
        fields = ["coin_search", "base_search", "start_date", "end_date"]
    
    

