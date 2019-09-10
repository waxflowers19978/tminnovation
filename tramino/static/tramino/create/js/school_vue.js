var vm_search = new Vue({
  el: '#school_vue',
  delimiters: ['[[', ']]'],
  data: {
    school_name: '',
    school_list: [],
    confirm_school_name: '',
    school_attribute: '',
    prefectures_name: '',
    city_name: '',
  },
  // `methods` オブジェクトの下にメソッドを定義します
  methods: {
    get_school: function (event) {
      axios.get(
        `/tramino/school_list?school_name=${this.school_name}`
      )

        .then(response=>{
          // console.log("axiosGetData:",response.data)
          this.school_list = response.data['data']
        })
        .catch(err=>{
          console.log("axiosGetErr",err)
        })

    },

    get_school_info: function(event) {
      csrftoken = Cookies.get('csrftoken');
      headers = {'X-CSRFToken': csrftoken};
      let params = new URLSearchParams();
      params.append('confirm_school_name', this.confirm_school_name);

      axios.post("/tramino/school_info/", params, {headers: headers})

        .then(response=>{
          var school_info = JSON.parse(response.data['data'])
          // var school_info = response.data["data"]
          this.school_attribute = school_info['school_attribute']
          this.prefectures_name = school_info['prefectures_name']
          this.city_name = school_info['city_name']
          // console.log(school_info);
        })
        .catch(err=>{
          console.log("axiosGetErr",err)
        })

    },
  }
})

var vm_form = new Vue({
  el: '#team_form',
  delimiters: ['[[', ']]'],
  data: {
  },
  methods: {
    organization_name_f: function () {
      // hogeのval1をfugaで参照出来る
      return vm_search.confirm_school_name
    },
    school_attribute_f: function () {
      return vm_search.school_attribute
    },
    prefectures_name_f: function () {
      return vm_search.prefectures_name
    },
    city_name_f: function () {
      return vm_search.city_name
    },
    create_team: function () {
      console.log('aiueo');
      axios.get(
        `/tramino/school_list`
      )

        .then(response=>{
        })
        .catch(err=>{
          console.log("axiosGetErr",err)
        })
      window.location.href = '/tramino/save_school_info'


    },
  }
})
