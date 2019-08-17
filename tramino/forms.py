# from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import TeamInformations, EventPostPool, EventApplyPool




class TeamInformationsForm(forms.ModelForm):

    class Meta:
        model = TeamInformations
        fields = '__all__'

class EventPostPoolForm(forms.Form):

    # class Meta:
    #     model = EventPostPool
    #     # fields = '__all__'
    #     widgets = {
    #         # 'event_date': AdminDateWidget(),
    #         # 'apply_deadline': AdminDateWidget(),
    #         'event_date': forms.SelectDateWidget,
    #         'apply_deadline': forms.SelectDateWidget,
    #     }

    # fields = ('event_name','event_description','event_picture','event_date','apply_deadline')
    event_name = forms.CharField(max_length = 50)
    event_description = forms.CharField(max_length = 300)
    event_picture = forms.ImageField()
    event_date = forms.DateField(required=True,widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'])#input_formats=['%Y-%m-%d','%Y/%m/%d',]
    apply_deadline = forms.DateField(required=True,widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'])

    # post_by = forms.ChoiceField(label=u'投稿元のチーム', choices=[])

class EventPostUpdateForm(forms.ModelForm):

    class Meta:
        model = EventPostPool
        fields = ('event_name','event_description','event_picture','event_date','apply_deadline')

        # fields = '__all__'
        widgets = {
            # 'event_date': AdminDateWidget(),
            # 'apply_deadline': AdminDateWidget(),
            'event_date': forms.SelectDateWidget,
            'apply_deadline': forms.SelectDateWidget,
        }

class MessageForm(forms.Form):
    any_message = forms.CharField(max_length = 300)

