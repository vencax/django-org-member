'''
Created on May 11, 2012

@author: vencax
'''
from django import forms
from .models import OrgMember

class ProfileForm(forms.ModelForm):
    class Meta:
        model = OrgMember
        fields = ('desc', 'place', 'tel', 'photo',)