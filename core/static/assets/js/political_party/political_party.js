$(function () {

  var loadForm = function (event) {

        var btn = $(this);
        $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-political_party").modal("show");
          },
          success: function (data) {
            $("#modal-political_party .modal-content").html(data.html_form);
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
          $("#political_party-table tbody").html(data.html_political_party_list);
          $("#modal-political_party").modal("hide");
        }
        else {
          $("#modal-political_party .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  }

    // Create election
    $(".js-create-political_party").click(loadForm);
    $("#modal-political_party").on("submit", ".js-political_party-create-form", saveForm);

    // Update election
    $("#political_party-table").on("click", ".js-update-political_party", loadForm);
    $("#modal-political_party").on("submit", ".js-political_party-update-form", saveForm);

    //Delection election
    $("#political_party-table").on("click", ".js-delete-political_party", loadForm);
    $("#modal-political_party").on("submit", ".js-political_party-delete-form", saveForm);
});
