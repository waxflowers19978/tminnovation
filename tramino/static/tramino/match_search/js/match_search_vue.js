
const PropsComp = {
    props: ['val'],
    template: "<img v-bind:src='val'>"
}

var vm = new Vue({
  el: '#match_search_vue',
  delimiters: ['[[', ']]'],
  data: {
    event_host_team: '',
    erea: '',
    kind: '',
    events: [
    ],
  },
  methods: {
    search: function(item) {
      csrftoken = Cookies.get('csrftoken');
      headers = {'X-CSRFToken': csrftoken};
      let params = new URLSearchParams();
      params.append('event_host_team', this.event_host_team);
      params.append('erea', this.erea);
      params.append('kind', this.kind);
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

    }
  },
  components: {
    'props-component': PropsComp
  }
})
