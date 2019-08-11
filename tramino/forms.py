# from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import TeamInformations, EventPostPool, EventApplyPool




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

# class EventApplyPoolForm(forms.ModelForm):
#     class Meta:
#         model = EventApplyPool
#         fields = '__all__'
#         # fields = ('','',)



class MyTeamsUpdateForm(forms.ModelForm):
    """チーム情報更新フォーム"""

    class Meta:
        model = TeamInformations
        fields = ('commander_name','commander_picture',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
