# from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import TeamInformations, EventPostPool, EventApplyPool

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

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
        fields = ('event_name','event_description','event_picture')
        # fields = ('event_name','event_description','event_picture','event_date','apply_deadline')

        # fields = '__all__'
        widgets = {
            # 'event_date': AdminDateWidget(),
            # 'apply_deadline': AdminDateWidget(),
            'event_date': forms.SelectDateWidget,
            'apply_deadline': forms.SelectDateWidget,
        }

class MessageForm(forms.Form):
    any_message = forms.CharField(max_length = 300)

class PastGameRecordsForm(forms.Form):
    game_category_list = [['練習試合','練習試合'],['公式戦','公式戦']]
    score_list = [['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9'],['10','10'],['11~','11~']]
    opponent_team_name = forms.CharField(max_length = 50)
    game_category = forms.ChoiceField(choices=game_category_list)
    my_score = forms.ChoiceField(choices=score_list)
    opponent_score = forms.ChoiceField(choices=score_list)
    game_date = forms.DateField(required=True,widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'])
    game_description = forms.CharField(max_length = 300)
