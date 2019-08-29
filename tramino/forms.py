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

# class TeamInformationsForm(forms.ModelForm):

#     class Meta:
#         model = TeamInformations
#         fields = '__all__'

class TeamInfoForm(forms.Form):
    club_list = [['サッカー','サッカー'],['野球','野球'],['ソフトボール','ソフトボール'],['テニス','テニス'],['ソフトテニス','ソフトテニス'],['バレーボール','バレーボール'],['バスケ','バスケ'],['バドミントン','バドミントン'],['柔道','柔道'],['剣道','剣道'],['卓球','卓球']]
    sex_list = [['女','女'],['男','男'],['混合チーム','混合チーム'],['その他','その他']]
    school_attribute_list = [['中学','中学'],['高校','高校']]
    prefectures_list = [['北海道','北海道'],['青森県','青森県'],['岩手県','岩手県'],['宮城県','宮城県'],['秋田県','秋田県'],['山形県','山形県'],['福島県','福島県'],['茨城県','茨城県'],['栃木県','栃木県'],['群馬県','群馬県'],['埼玉県','埼玉県'],['千葉県','千葉県'],['東京都','東京都'],['神奈川県','神奈川県'],['新潟県','新潟県'],['富山県','富山県'],['石川県','石川県'],['福井県','福井県'],['山梨県','山梨県'],['長野県','長野県'],['岐阜県','岐阜県'],['静岡県','静岡県'],['愛知県','愛知県'],['三重県','三重県'],['滋賀県','滋賀県'],['京都府','京都府'],['大阪府','大阪府'],['兵庫県','兵庫県'],['奈良県','奈良県'],['和歌山県','和歌山県'],['鳥取県','鳥取県'],['島根県','島根県'],['岡山県','岡山県'],['広島県','広島県'],['山口県','山口県'],['徳島県','徳島県'],['香川県','香川県'],['愛媛県','愛媛県'],['高知県','高知県'],['福岡県','福岡県'],['佐賀県','佐賀県'],['長崎県','長崎県'],['熊本県','熊本県'],['大分県','大分県'],['宮崎県','宮崎県'],['鹿児島県','鹿児島県'],['沖縄県','沖縄県']]
    practice_frequency_list = [['～週３','～週３'],['週４～週５','週４～週５'],['週６～週７','週６～週７']]
    number_of_members_list = [['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9'],['10','10'],['11','11'],['12','12'],['13','13'],['14','14'],['15','15'],['16','16'],['17','17'],['18','18'],['19','19'],['20','20'],['21','21'],['22','22'],['23','23'],['24','24'],['25','25'],['26','26'],['27','27'],['28','28'],['29','29'],['30','30'],['31','31'],['32','32'],['33','33'],['34','34'],['35','35'],['36','36'],['37','37'],['38','38'],['39','39'],['40','40'],['41','41'],['42','42'],['43','43'],['44','44'],['45','45'],['46','46'],['47','47'],['48','48'],['49','49'],['50','50'],['51','51'],['52','52'],['53','53'],['54','54'],['55','55'],['56','56'],['57','57'],['58','58'],['59','59'],['60','60'],['61','61'],['62','62'],['63','63'],['64','64'],['65','65'],['66','66'],['67','67'],['68','68'],['69','69'],['70','70'],['71','71'],['72','72'],['73','73'],['74','74'],['75','75'],['76','76'],['77','77'],['78','78'],['79','79'],['80','80'],['81','81'],['82','82'],['83','83'],['84','84'],['85','85'],['86','86'],['87','87'],['88','88'],['89','89'],['90','90'],['91','91'],['92','92'],['93','93'],['94','94'],['95','95'],['96','96'],['97','97'],['98','98'],['99','99'],['100','100'],['101~','101~']]
    achievement_list = [['全国大会出場常連レベル','全国大会出場常連レベル'],['全国大会出場レベル','全国大会出場レベル'],['都道府県大会常連レベル','都道府県大会常連レベル'],['都道府県大会出場レベル','都道府県大会出場レベル'],['地区大会入賞レベル','地区大会入賞レベル'],['地区大会常連レベル','地区大会常連レベル']]
    activity_place_list = [['校内のみ','校内のみ'],['校外のみ','校外のみ'],['両方','両方'],['その他','その他']]

    organization_name = forms.CharField(max_length = 30)
    club_name = forms.ChoiceField(choices=club_list)
    sex = forms.ChoiceField(choices=sex_list)
    school_attribute = forms.ChoiceField(choices=school_attribute_list)
    prefectures_name = forms.ChoiceField(choices=prefectures_list)
    city_name = forms.CharField(max_length = 30)
    activity_place = forms.ChoiceField(choices=activity_place_list)
    # team_picture = forms.ImageField()
    # url = forms.CharField(max_length = 200)
    achievement = forms.ChoiceField(choices=achievement_list)
    # practice_frequency = forms.CharField(max_length = 30)
    number_of_members = forms.ChoiceField(choices=number_of_members_list)
    commander_name = forms.CharField(max_length = 30)
    # commander_career = forms.CharField(max_length = 30)
    # commander_picture = forms.ImageField()
    # commander_introduction = forms.CharField(max_length = 30)

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
    event_date = forms.DateField(required=True,widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'])#input_formats=['%Y-%m-%d','%Y/%m/%d',]
    apply_deadline = forms.DateField(required=True,widget=forms.DateInput(attrs={"type": "date"}),input_formats=['%Y-%m-%d'])

    # post_by = forms.ChoiceField(label=u'投稿元のチーム', choices=[])

class EventPostUpdateForm(forms.ModelForm):

    class Meta:
        model = EventPostPool
        fields = ('event_name','event_description')
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
