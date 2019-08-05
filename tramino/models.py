from django.db import models

# Create your models here.


class team_infomation(models.Model):

    sex_list = [['女','女'],['男','男'],['混合チーム','混合チーム'],['その他','その他']]
    school_attribute_list = [['中学','中学'],['高校','高校']]
    prefectures_list = [['北海道','北海道'],['青森県','青森県'],['岩手県','岩手県'],['宮城県','宮城県'],['秋田県','秋田県'],['山形県','山形県'],['福島県','福島県'],['茨城県','茨城県'],['栃木県','栃木県'],['群馬県','群馬県'],['埼玉県','埼玉県'],['千葉県','千葉県'],['東京都','東京都'],['神奈川県','神奈川県'],['新潟県','新潟県'],['富山県','富山県'],['石川県','石川県'],['福井県','福井県'],['山梨県','山梨県'],['長野県','長野県'],['岐阜県','岐阜県'],['静岡県','静岡県'],['愛知県','愛知県'],['三重県','三重県'],['滋賀県','滋賀県'],['京都府','京都府'],['大阪府','大阪府'],['兵庫県','兵庫県'],['奈良県','奈良県'],['和歌山県','和歌山県'],['鳥取県','鳥取県'],['島根県','島根県'],['岡山県','岡山県'],['広島県','広島県'],['山口県','山口県'],['徳島県','徳島県'],['香川県','香川県'],['愛媛県','愛媛県'],['高知県','高知県'],['福岡県','福岡県'],['佐賀県','佐賀県'],['長崎県','長崎県'],['熊本県','熊本県'],['大分県','大分県'],['宮崎県','宮崎県'],['鹿児島県','鹿児島県'],['沖縄県','沖縄県']]
    practice_frequency_list = [['～週３','～週３'],['週４～週５','週４～週５'],['週６～週７','週６～週７']]
    number_of_members_list = [['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9'],['10','10'],['11','11'],['12','12'],['13','13'],['14','14'],['15','15'],['16','16'],['17','17'],['18','18'],['19','19'],['20','20'],['21','21'],['22','22'],['23','23'],['24','24'],['25','25'],['26','26'],['27','27'],['28','28'],['29','29'],['30','30'],['31','31'],['32','32'],['33','33'],['34','34'],['35','35'],['36','36'],['37','37'],['38','38'],['39','39'],['40','40'],['41','41'],['42','42'],['43','43'],['44','44'],['45','45'],['46','46'],['47','47'],['48','48'],['49','49'],['50','50'],['51','51'],['52','52'],['53','53'],['54','54'],['55','55'],['56','56'],['57','57'],['58','58'],['59','59'],['60','60'],['61','61'],['62','62'],['63','63'],['64','64'],['65','65'],['66','66'],['67','67'],['68','68'],['69','69'],['70','70'],['71','71'],['72','72'],['73','73'],['74','74'],['75','75'],['76','76'],['77','77'],['78','78'],['79','79'],['80','80'],['81','81'],['82','82'],['83','83'],['84','84'],['85','85'],['86','86'],['87','87'],['88','88'],['89','89'],['90','90'],['91','91'],['92','92'],['93','93'],['94','94'],['95','95'],['96','96'],['97','97'],['98','98'],['99','99'],['100','100'],['101~','101~']]


    #チームに関する情報
    organization_name = models.CharField(max_length = 30)
    club_name = models.CharField(max_length = 30)
    sex = models.CharField(max_length = 30, choices=sex_list)
    school_attribute = models.CharField(max_length = 30, choices=school_attribute_list)
    prefectures_name = models.CharField(max_length = 30, choices=prefectures_list)
    city_name = models.CharField(max_length = 50, null=True, blank=True)
    activity_place = models.CharField(max_length = 30)
    #team_picture = models.ImageField(upload_to="image/")
    url = models.CharField(max_length = 200, null=True, blank=True)
    achievement = models.CharField(max_length = 30, null=True, blank=True)
    practice_frequency = models.CharField(max_length = 30, choices=practice_frequency_list, null=True, blank=True)
    number_of_members = models.CharField(max_length = 30, choices=number_of_members_list, null=True, blank=True)

    #顧問に関する情報
    commander_name = models.CharField(max_length = 30)
    #position = models.CharField(max_length = 30)
    commander_career = models.CharField(max_length = 400, null=True, blank=True)
    #commander_picture = models.ImageField(upload_to="image/")
    commander_introduction = models.CharField(max_length = 2000, null=True, blank=True)



