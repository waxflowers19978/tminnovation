
var vm = new Vue({
  el: '#match_search_vue',
  delimiters: ['[[', ']]'],
  data: {
    event_host_team: '',
    prefecture: '',
    prefecture_list: [],
    club_name: '',
    club_name_list: [],
    number_of_members: '',
    number_of_members_list: [],
    team_level:'',
    team_level_list: [],
    date1: '',
    date2: '',
    events: [],
  },
  methods: {
    search: function(item) {
      csrftoken = Cookies.get('csrftoken');
      headers = {'X-CSRFToken': csrftoken};
      let params = new URLSearchParams();
      params.append('event_host_team', this.event_host_team);
      params.append('prefecture', this.prefecture);
      params.append('club_name', this.club_name);
      params.append('number_of_members', this.number_of_members);
      params.append('achievement', this.team_level)
      params.append('date1', this.date1);
      params.append('date2', this.date2);
      axios.post("/tramino/match_refine/", params, {headers: headers})

        .then(response=>{
          // console.log(response.data['data'])
          // var event_list = JSON.parse(response.data)
          var event_list = JSON.parse(response.data['data'])
          // console.log(event_list)
          this.events = event_list
        })
        .catch(err=>{
          console.log("axiosGetErr",err)
        })

    },
  },
  created: function () {
    var dt = new Date();
    var y = dt.getFullYear();
    var m = ("00" + (dt.getMonth()+1)).slice(-2);
    var d = ("00" + dt.getDate()).slice(-2);
    var date1 = y + "-" + m + "-" + d;
    var date2 = y + "-" + m + "-" + d;
    this.date1 = date1;
    this.date2 = date2;

  }
})


vm.prefecture_list = [['北海道','北海道'],['青森県','青森県'],['岩手県','岩手県'],['宮城県','宮城県'],['秋田県','秋田県'],['山形県','山形県'],['福島県','福島県'],['茨城県','茨城県'],['栃木県','栃木県'],['群馬県','群馬県'],['埼玉県','埼玉県'],['千葉県','千葉県'],['東京都','東京都'],['神奈川県','神奈川県'],['新潟県','新潟県'],['富山県','富山県'],['石川県','石川県'],['福井県','福井県'],['山梨県','山梨県'],['長野県','長野県'],['岐阜県','岐阜県'],['静岡県','静岡県'],['愛知県','愛知県'],['三重県','三重県'],['滋賀県','滋賀県'],['京都府','京都府'],['大阪府','大阪府'],['兵庫県','兵庫県'],['奈良県','奈良県'],['和歌山県','和歌山県'],['鳥取県','鳥取県'],['島根県','島根県'],['岡山県','岡山県'],['広島県','広島県'],['山口県','山口県'],['徳島県','徳島県'],['香川県','香川県'],['愛媛県','愛媛県'],['高知県','高知県'],['福岡県','福岡県'],['佐賀県','佐賀県'],['長崎県','長崎県'],['熊本県','熊本県'],['大分県','大分県'],['宮崎県','宮崎県'],['鹿児島県','鹿児島県'],['沖縄県','沖縄県']]

vm.club_name_list = [['サッカー','サッカー'],['野球','野球'],['ソフトボール','ソフトボール'],['テニス','テニス'],['ソフトテニス','ソフトテニス'],['バレーボール','バレーボール'],['バスケ','バスケ'],['バドミントン','バドミントン'],['柔道','柔道'],['剣道','剣道'],['卓球','卓球']]


vm.number_of_members_list =[['1','1'],['2','2'],['3','3'],['4','4'],['5','5'],['6','6'],['7','7'],['8','8'],['9','9'],['10','10'],['11','11'],['12','12'],['13','13'],['14','14'],['15','15'],['16','16'],['17','17'],['18','18'],['19','19'],['20','20'],['21','21'],['22','22'],['23','23'],['24','24'],['25','25'],['26','26'],['27','27'],['28','28'],['29','29'],['30','30'],['31','31'],['32','32'],['33','33'],['34','34'],['35','35'],['36','36'],['37','37'],['38','38'],['39','39'],['40','40'],['41','41'],['42','42'],['43','43'],['44','44'],['45','45'],['46','46'],['47','47'],['48','48'],['49','49'],['50','50'],['51','51'],['52','52'],['53','53'],['54','54'],['55','55'],['56','56'],['57','57'],['58','58'],['59','59'],['60','60'],['61','61'],['62','62'],['63','63'],['64','64'],['65','65'],['66','66'],['67','67'],['68','68'],['69','69'],['70','70'],['71','71'],['72','72'],['73','73'],['74','74'],['75','75'],['76','76'],['77','77'],['78','78'],['79','79'],['80','80'],['81','81'],['82','82'],['83','83'],['84','84'],['85','85'],['86','86'],['87','87'],['88','88'],['89','89'],['90','90'],['91','91'],['92','92'],['93','93'],['94','94'],['95','95'],['96','96'],['97','97'],['98','98'],['99','99'],['100','100'],['101~','101~']]


vm.team_level_list = [['全国大会出場常連レベル','全国大会出場常連レベル'],['全国大会出場レベル','全国大会出場レベル'],['都道府県大会常連レベル','都道府県大会常連レベル'],['都道府県大会出場レベル','都道府県大会出場レベル'],['地区大会入賞レベル','地区大会入賞レベル'],['地区大会常連レベル','地区大会常連レベル']]


// input[type='date']に対応しているか調べる関数
function hasInputTypeDate() {
    var elm = document.createElement('input');
    elm.setAttribute('type', 'date');
    elm.value = 1;
    return elm.value != 1;
}