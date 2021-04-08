function get_data(url) {
  $.ajax({
    url: url, success: function (result, status) {
      $("#data_div").html(JSON.stringify(result));
    }
  });
}