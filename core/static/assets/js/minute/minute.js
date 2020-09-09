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

var room = 1;
function education_fields() {

    room++;
    var objTo = document.getElementById('education_fields')
    var divtest = document.createElement("div");
	divtest.setAttribute("class", "form-group removeclass"+room);
	var rdiv = 'removeclass'+room;
    divtest.innerHTML = '<div class="form-group col-sm-2 col-md-2"> <a  type="button" id ="" class="btn btn-info btn-sm" title="Ajouter un Parti"><i id="pop" class="fa fa-plus icon-large"></i> </a></div><div class="form-group col-sm-4 col-md-3 nopadding"><div class="form-group"><div class="input-group"> <select class="form-control" id="educationDate" name="educationDate[]"><option value="">Parti Politique</option><option value="ufr">UFR</option><option value="ufdg">UFDG</option><option value="rpg">RPG</option> </select><div class="input-group-btn"> <button class="btn btn-danger" type="button" onclick="remove_education_fields('+ room +');"> <span class="glyphicon glyphicon-minus" aria-hidden="true"></span> </button></div></div></div><div class="form-group col-sm-4 col-md-3 nopadding"><div class="form-group"> <input type="text" class="form-control" id="vote" name="vote[]" value="" placeholder="vote"></div></div><div class="clear"></div>';

    objTo.appendChild(divtest)
}
   function remove_education_fields(rid) {
	   $('.removeclass'+rid).remove();
   }

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





