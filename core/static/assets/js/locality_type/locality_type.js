$(function () {

  var loadForm = function (event) {

        var btn = $(this);
        $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal").modal("show");
          },
          success: function (data) {
            $("#modal .modal-content").html(data.html_form);
          }
       });
    }

  var saveForm = function () {

    var thisForm = $(this)
    var actionEndpoint = thisForm.attr("action")
    var httpMethod = thisForm.attr("method")
    var fromData = thisForm.serialize()

    $.ajax({
      url: actionEndpoint,
      data: fromData,
      type: httpMethod,
      dataType: 'json',
     success: function (data) {
        if (data.form_is_valid) {
          $("#table tbody").html(data.html_list);
          $("#modal").modal("hide");
        }
        else {
          $("#modal .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  }

    // Create election
    $(".js-create").click(loadForm);
    $("#modal").on("submit", ".js-create-form", saveForm);

    // Update election
    $("#table").on("click", ".js-update", loadForm);
    $("#modal").on("submit", ".js-update-form", saveForm);

    //Delection election
    $("#table").on("click", ".js-delete", loadForm);
    $("#modal").on("submit", ".js-delete-form", saveForm);
});
