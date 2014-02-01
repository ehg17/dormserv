from django import forms
from cal.models import Item

class ItemForm(forms.ModelForm):
	class Meta:
		fields = ('wanted',)
