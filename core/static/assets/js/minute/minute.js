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


function upload(event) {
    event.preventDefault();
    var data = new FormData(this);

    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
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



function showModal(event) {
    event.preventDefault();
    var id = $(this).data('id');
    $('#imagepreview').attr('src', id);
    $('#imagemodal').modal('show');
}
/*
    $('.formset_row-{{ formset.prefix }}').formset({
        addText: 'Ajouter un parti',
        deleteText: 'remove',
        prefix: 'minute_details_set'
    });*/

    $('.show').click( showModal);
    // Create election
    $(".js-create").click(loadForm);
    $("#modal").on("submit", ".js-create-form", upload);

    // Update election
    $("#table").on("click", ".js-update", loadForm);
    $("#modal").on("submit", ".js-update-form", saveForm);

    //Delection election
    $("#table").on("click", ".js-delete", loadForm);
    $("#modal").on("submit", ".js-delete-form", saveForm);

});




