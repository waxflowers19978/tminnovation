# Generated by Django 2.1 on 2019-08-09 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tramino.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', tramino.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EventApplyPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventPostPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=50)),
                ('event_description', models.CharField(max_length=300)),
                ('event_picture', models.ImageField(blank=True, default='SOME STRING', null=True, upload_to=tramino.models.get_event)),
                ('event_date', models.DateField(verbose_name='date published')),
                ('apply_deadline', models.DateField(verbose_name='date published')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteEventPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('event_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_favorites', to='tramino.EventPostPool')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteTeamPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PastGameRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent_team_name', models.CharField(max_length=50)),
                ('game_category', models.CharField(choices=[['練習試合', '練習試合'], ['公式戦', '公式戦']], max_length=30)),
                ('my_score', models.CharField(choices=[['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10'], ['11~', '11~']], max_length=30)),
                ('opponent_score', models.CharField(choices=[['0', '0'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10'], ['11~', '11~']], max_length=30)),
                ('game_date', models.DateField(verbose_name='date published')),
                ('game_description', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamInformations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=30)),
                ('club_name', models.CharField(max_length=30)),
                ('sex', models.CharField(choices=[['女', '女'], ['男', '男'], ['混合チーム', '混合チーム'], ['その他', 'その他']], max_length=30)),
                ('school_attribute', models.CharField(choices=[['中学', '中学'], ['高校', '高校']], max_length=30)),
                ('prefectures_name', models.CharField(choices=[['北海道', '北海道'], ['青森県', '青森県'], ['岩手県', '岩手県'], ['宮城県', '宮城県'], ['秋田県', '秋田県'], ['山形県', '山形県'], ['福島県', '福島県'], ['茨城県', '茨城県'], ['栃木県', '栃木県'], ['群馬県', '群馬県'], ['埼玉県', '埼玉県'], ['千葉県', '千葉県'], ['東京都', '東京都'], ['神奈川県', '神奈川県'], ['新潟県', '新潟県'], ['富山県', '富山県'], ['石川県', '石川県'], ['福井県', '福井県'], ['山梨県', '山梨県'], ['長野県', '長野県'], ['岐阜県', '岐阜県'], ['静岡県', '静岡県'], ['愛知県', '愛知県'], ['三重県', '三重県'], ['滋賀県', '滋賀県'], ['京都府', '京都府'], ['大阪府', '大阪府'], ['兵庫県', '兵庫県'], ['奈良県', '奈良県'], ['和歌山県', '和歌山県'], ['鳥取県', '鳥取県'], ['島根県', '島根県'], ['岡山県', '岡山県'], ['広島県', '広島県'], ['山口県', '山口県'], ['徳島県', '徳島県'], ['香川県', '香川県'], ['愛媛県', '愛媛県'], ['高知県', '高知県'], ['福岡県', '福岡県'], ['佐賀県', '佐賀県'], ['長崎県', '長崎県'], ['熊本県', '熊本県'], ['大分県', '大分県'], ['宮崎県', '宮崎県'], ['鹿児島県', '鹿児島県'], ['沖縄県', '沖縄県']], max_length=30)),
                ('city_name', models.CharField(blank=True, max_length=50, null=True)),
                ('activity_place', models.CharField(max_length=30)),
                ('team_picture', models.ImageField(default='SOME STRING', upload_to=tramino.models.get_team)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('achievement', models.CharField(blank=True, max_length=30, null=True)),
                ('practice_frequency', models.CharField(blank=True, choices=[['～週３', '～週３'], ['週４～週５', '週４～週５'], ['週６～週７', '週６～週７']], max_length=30, null=True)),
                ('number_of_members', models.CharField(blank=True, choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6'], ['7', '7'], ['8', '8'], ['9', '9'], ['10', '10'], ['11', '11'], ['12', '12'], ['13', '13'], ['14', '14'], ['15', '15'], ['16', '16'], ['17', '17'], ['18', '18'], ['19', '19'], ['20', '20'], ['21', '21'], ['22', '22'], ['23', '23'], ['24', '24'], ['25', '25'], ['26', '26'], ['27', '27'], ['28', '28'], ['29', '29'], ['30', '30'], ['31', '31'], ['32', '32'], ['33', '33'], ['34', '34'], ['35', '35'], ['36', '36'], ['37', '37'], ['38', '38'], ['39', '39'], ['40', '40'], ['41', '41'], ['42', '42'], ['43', '43'], ['44', '44'], ['45', '45'], ['46', '46'], ['47', '47'], ['48', '48'], ['49', '49'], ['50', '50'], ['51', '51'], ['52', '52'], ['53', '53'], ['54', '54'], ['55', '55'], ['56', '56'], ['57', '57'], ['58', '58'], ['59', '59'], ['60', '60'], ['61', '61'], ['62', '62'], ['63', '63'], ['64', '64'], ['65', '65'], ['66', '66'], ['67', '67'], ['68', '68'], ['69', '69'], ['70', '70'], ['71', '71'], ['72', '72'], ['73', '73'], ['74', '74'], ['75', '75'], ['76', '76'], ['77', '77'], ['78', '78'], ['79', '79'], ['80', '80'], ['81', '81'], ['82', '82'], ['83', '83'], ['84', '84'], ['85', '85'], ['86', '86'], ['87', '87'], ['88', '88'], ['89', '89'], ['90', '90'], ['91', '91'], ['92', '92'], ['93', '93'], ['94', '94'], ['95', '95'], ['96', '96'], ['97', '97'], ['98', '98'], ['99', '99'], ['100', '100'], ['101~', '101~']], max_length=30, null=True)),
                ('commander_name', models.CharField(max_length=30)),
                ('commander_career', models.CharField(blank=True, max_length=400, null=True)),
                ('commander_picture', models.ImageField(default='SOME STRING', upload_to=tramino.models.get_commander)),
                ('commander_introduction', models.CharField(blank=True, max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_informations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pastgamerecords',
            name='register_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='past_game_records', to='tramino.TeamInformations'),
        ),
        migrations.AddField(
            model_name='favoriteteampool',
            name='guest_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipient_team', to='tramino.TeamInformations'),
        ),
        migrations.AddField(
            model_name='favoriteteampool',
            name='host_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_sender_team', to='tramino.TeamInformations'),
        ),
        migrations.AddField(
            model_name='favoriteeventpool',
            name='guest_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_favorites', to='tramino.TeamInformations'),
        ),
        migrations.AddField(
            model_name='eventpostpool',
            name='event_host_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_posts', to='tramino.TeamInformations'),
        ),
        migrations.AddField(
            model_name='eventapplypool',
            name='event_post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_applies', to='tramino.EventPostPool'),
        ),
        migrations.AddField(
            model_name='eventapplypool',
            name='guest_team_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_applies', to='tramino.TeamInformations'),
        ),
    ]
