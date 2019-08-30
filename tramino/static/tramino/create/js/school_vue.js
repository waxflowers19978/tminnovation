var vm = new Vue({
  el: '#school_vue',
  delimiters: ['[[', ']]'],
  data: {
    school_name: '',
    school_list: [],
  },
  // `methods` オブジェクトの下にメソッドを定義します
  methods: {
    aiueo: function (event) {

      // axios.get("/tramino/school_list/")
      axios.get(
        `/tramino/school_list?school_name=${this.school_name}`
      )

        .then(response=>{
          console.log("axiosGetData:",response.data)
          this.school_list = response.data['data']
        })
        .catch(err=>{
          console.log("axiosGetErr",err)
        })

    },
  }
})
