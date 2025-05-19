from django import forms
from .models import LostItem, FoundItem


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = '__all__'  # or specify fields explicitly

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = '__all__'
        
        # fields = [
        #     'name', 'email', 'phone', 
        #     'item_name', 'item_type', 
        #     'color', 'brand', 'date_lost', 
        #     'location_lost', 'details', 'photo'
        # ]

from django import forms
from .models import Claim


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claimant_name', 'claimant_email', 'claimant_phone', 'claim_message']
