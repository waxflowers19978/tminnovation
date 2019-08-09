# from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import TeamInformations, EventPostPool




class TeamInformationsForm(forms.ModelForm):

    class Meta:
        model = TeamInformations
        fields = '__all__'

class EventPostPoolForm(forms.ModelForm):
    class Meta:
        model = EventPostPool
        fields = '__all__'
        widgets = {
            # 'event_date': AdminDateWidget(),
            # 'apply_deadline': AdminDateWidget(),
            'event_date': forms.SelectDateWidget,
            'apply_deadline': forms.SelectDateWidget,
        }
