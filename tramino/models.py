from django.db import models
import datetime
from django.utils import timezone

import os
import uuid

"""
画像の保存path名を一意に設定
"""
def get_team(self, filename):
    prefix = 'team/team/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension
def get_commander(self, filename):
    prefix = 'team/commander/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension
def get_event(self, filename):
    prefix = 'event/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension

# Create your models here.

#create table tramino_teaminformations(id serial NOT NULL PRIMARY KEY, organization_name varchar(30) NOT NULL, club_name varchar(30) NOT NULL, sex varchar(30) NOT NULL, school_attribute varchar(30) NOT NULL, prefectures_name varchar(30) NOT NULL, city_name varchar(50), activity_place varchar(30) NOT NULL, url varchar(200), achievement varchar(30), practice_frequency varchar(30), number_of_members varchar(30), commander_name varchar(30) NOT NULL, commander_career varchar(30), commander_introduction varchar(30), created_at date);

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Transpose

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email


class TeamInformations(models.Model):

    sex_list = [['女','女'],['男','男'],['混合チーム','混合チーム'],['その他','その他']]
    school_attribute_list = [['中学','中学'],['高校','高校']]
    prefectures_list = [['北海道','北海道'],['青森県','青森県'],['岩手県','岩手県'],['宮城県','宮城県'],['秋田県','秋田県'],['山形県','山形県'],['福島県','福島県'],['茨城県','茨城県'],['栃木県','栃木県'],['群馬県','群馬県'],['埼玉県','埼玉県'],['千葉県','千葉県'],['東京都','東京都'],['神奈川県','神奈川県'],['新潟県','新潟県'],['富山県','富山県'],['石川県','石川県'],['福井県','福井県'],['山梨県','山梨県'],['長野県','長野県'],['岐阜県','岐阜県'],['静岡県','静岡県'],['愛知県','愛知県'],['三重県','三重県'],['滋賀県','滋賀県'],['京都府','京都府'],['大阪府','大阪府'],['兵庫県','兵庫県'],['奈良県','奈良県'],['和歌山県','和歌山県'],['鳥取県','鳥取県'],['島根県','島根県'],['岡山県','岡山県'],['広島県','広島県'],['山口県','山口県'],['徳島県','徳島県'],['香川県','香川県'],['愛媛県','愛媛県'],['高知県','高知県'],['福岡県','福岡県'],['佐賀県','佐賀県'],['長崎県','長崎県'],['熊本県','熊本県'],['大分県','大分県'],['宮崎県','宮崎県'],['鹿児島県','鹿児島県'],['沖縄県','沖縄県']]
    practice_frequency_list = [['～週３','～週３'],['週４～週５','週４～週５'],['週６～週７','週６～週７']]
    number_of_members_list = [['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9'],['10','10'],['11','11'],['12','12'],['13','13'],['14','14'],['15','15'],['16','16'],['17','17'],['18','18'],['19','19'],['20','20'],['21','21'],['22','22'],['23','23'],['24','24'],['25','25'],['26','26'],['27','27'],['28','28'],['29','29'],['30','30'],['31','31'],['32','32'],['33','33'],['34','34'],['35','35'],['36','36'],['37','37'],['38','38'],['39','39'],['40','40'],['41','41'],['42','42'],['43','43'],['44','44'],['45','45'],['46','46'],['47','47'],['48','48'],['49','49'],['50','50'],['51','51'],['52','52'],['53','53'],['54','54'],['55','55'],['56','56'],['57','57'],['58','58'],['59','59'],['60','60'],['61','61'],['62','62'],['63','63'],['64','64'],['65','65'],['66','66'],['67','67'],['68','68'],['69','69'],['70','70'],['71','71'],['72','72'],['73','73'],['74','74'],['75','75'],['76','76'],['77','77'],['78','78'],['79','79'],['80','80'],['81','81'],['82','82'],['83','83'],['84','84'],['85','85'],['86','86'],['87','87'],['88','88'],['89','89'],['90','90'],['91','91'],['92','92'],['93','93'],['94','94'],['95','95'],['96','96'],['97','97'],['98','98'],['99','99'],['100','100'],['101~','101~']]
    achievement_list = [['全国大会優勝レベル','全国大会優勝レベル'],['全国大会入賞レベル','全国大会入賞レベル'],['全国大会出場常連レベル','全国大会出場常連レベル'],['全国大会出場レベル','全国大会出場レベル'],['都道府県大会入賞レベル','都道府県大会入賞レベル'],['都道府県大会常連レベル','都道府県大会常連レベル'],['都道府県大会出場レベル','都道府県 大会出場レベル'],['地区大会入賞レベル','地区大会入賞レベル'],['地区大会常連レベル','地区大会常連レベル']]
    #チームに関する情報
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_informations')
    organization_name = models.CharField(max_length = 30)
    club_name = models.CharField(max_length = 30)
    sex = models.CharField(max_length = 30, choices=sex_list)
    school_attribute = models.CharField(max_length = 30, choices=school_attribute_list)
    prefectures_name = models.CharField(max_length = 30, choices=prefectures_list)
    city_name = models.CharField(max_length = 50, null=True, blank=True)
    activity_place = models.CharField(max_length = 30)
    # team_picture = models.ImageField(upload_to=get_team, default='SOME STRING')# SOME STRINGはNO CHANGEでお願い
    team_picture = ProcessedImageField(upload_to=get_team,
                                            processors=[Transpose(),ResizeToFill(800, 350)],
                                            format='JPEG',
                                            options={'quality': 60},
                                            default='SOME STRING')# SOME STRINGはNO CHANGEでお願い

    url = models.CharField(max_length = 200, null=True, blank=True)
    achievement = models.CharField(max_length = 30, choices=achievement_list, null=True, blank=True)
    practice_frequency = models.CharField(max_length = 30, choices=practice_frequency_list, null=True, blank=True)
    number_of_members = models.CharField(max_length = 30, choices=number_of_members_list, null=True, blank=True)

    #顧問に関する情報
    commander_name = models.CharField(max_length = 30)
    #position = models.CharField(max_length = 30)
    commander_career = models.CharField(max_length = 400, null=True, blank=True)
    # commander_picture = models.ImageField(upload_to=get_commander, default='SOME STRING')# SOME STRINGはNO CHANGEでお願い
    commander_picture = ProcessedImageField(upload_to=get_commander, 
                                            processors=[Transpose(),ResizeToFill(200, 200)],
                                            format='JPEG',
                                            options={'quality': 60},
                                            default='SOME STRING')# SOME STRINGはNO CHANGEでお願い

    commander_introduction = models.CharField(max_length = 2000, null=True, blank=True)

    # thumbnail = ImageSpecField(source='commander_picture',
    #                         processors=[ResizeToFill(250,250)],
    #                         format="JPEG",
    #                         options={'quality': 60}
    #                         )

    #created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        # created_at = self.created_at
        # created_at = created_at + datetime.timedelta(hours=9)
        # return created_at.strftime('%Y/%m/%d %H:%M')+ self.organization_name+self.club_name
        return self.organization_name + ' : '  + self.user.email

class EventPostPool(models.Model):
    event_host_team = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='event_posts')
    event_name = models.CharField(max_length = 50)
    event_description = models.CharField(max_length = 300)
    event_picture = models.ImageField(upload_to=get_event, default='SOME STRING', null=True, blank=True)
    # event_picture = models.ImageField(upload_to="event/", null=True, blank=True)
    event_date = models.DateField('date published')
    apply_deadline = models.DateField('date published')
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.event_host_team.organization_name + ' : ' +self.event_name

class EventPostComment(models.Model):
    message = models.TextField(max_length=4000)
    post = models.ForeignKey(EventPostPool, on_delete=models.CASCADE, related_name='event_post_comments')
    guest_team_id = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='commenter_team', null=True, blank=True)
    good = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

class EventApplyPool(models.Model):
    event_post_id = models.ForeignKey(EventPostPool, on_delete=models.CASCADE, related_name='event_applies')
    guest_team_id = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='event_applies')
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.event_post_id.event_host_team.organization_name + ' : ' + self.event_post_id.event_name + ' applyed by ' +self.guest_team_id.organization_name

class FavoriteEventPool(models.Model):
    event_post_id = models.ForeignKey(EventPostPool, on_delete=models.CASCADE, related_name='event_favorites')
    guest_team_id = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='event_favorites')
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.event_post_id.event_host_team.organization_name + ' : ' + self.event_post_id.event_name + ' favorited by ' +self.guest_team_id.organization_name

class FavoriteTeamPool(models.Model):
    host_team_id = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='favorite_sender_team')
    guest_team_id = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='favorite_recipient_team')
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.host_team_id.organization_name + ' favorited by ' +self.guest_team_id.organization_name

class PastGameRecords(models.Model):
    game_category_list = [['練習試合','練習試合'],['公式戦','公式戦']]
    score_list = [['0','0'],['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9'],['10','10'],['11~','11~']]

    register_team_id = models.ForeignKey(TeamInformations, on_delete=models.CASCADE, related_name='past_game_records')
    opponent_team_name = models.CharField(max_length = 50)
    game_category = models.CharField(max_length = 30, choices=game_category_list)
    my_score = models.CharField(max_length = 30, choices=score_list)
    opponent_score = models.CharField(max_length = 30, choices=score_list)
    game_date = models.DateField('date published')
    game_description = models.CharField(max_length = 300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.register_team_id.organization_name + ' VS ' +self.opponent_team_name + ' : ' + self.my_score + ' - ' + self.opponent_score
