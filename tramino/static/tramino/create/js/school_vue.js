var vm = new Vue({
  el: "#school_vue",
  delimiters: ['[[', ']]'],
  data: {
    "school_name": ""
  },
  methods: {
    onInput: function() {
      axios
        .get('/tramino/create')
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
});
