$(function () {

  var loadForm = function (event) {

        var btn = $(this);
        $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-sms").modal("show");
          },
          success: function (data) {
            $("#modal-sms .modal-content").html(data.html_form);
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
          $("#sms-table tbody").html(data.html_sms_list);
          $("#modal-sms").modal("hide");
        }
        else {
          $("#modal-sms .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  }

    // Create election
    $(".js-create-sms").click(loadForm);
    $("#modal-sms").on("submit", ".js-sms-create-form", saveForm);

    // Update election
    $("#sms-table").on("click", ".js-update-sms", loadForm);
    $("#modal-sms").on("submit", ".js-sms-update-form", saveForm);

    //Delection election
    $("#sms-table").on("click", ".js-delete-sms", loadForm);
    $("#modal-sms").on("submit", ".js-sms-delete-form", saveForm);
});
