$(function () {

  var loadForm = function () {

        var btn = $(this);
        $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal-election").modal("show");
          },
          success: function (data) {
            $("#modal-election .modal-content").html(data.html_form);
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
          $("#election-table tbody").html(data.html_election_list);
          $("#modal-election").modal("hide");
        }
        else {
          $("#modal-election .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  }


    // Create election
    $(".js-create-election").click(loadForm);
    $("#modal-election").on("submit", ".js-election-create-form", saveForm);
/*
    // Update election
    $("#election-table").on("click", ".js-update-election", loadForm);
    $("#modal-election").on("submit", ".js-election-update-form", saveForm);

    //Delection election
    $("#election-table").on("click", ".js-delete-election", loadForm);
    $("#modal-election").on("submit", ".js-election-delete-form", saveForm);*/
});


/*
$(document).click(function(){
      var electionForm = $(".js-create-election")
      electionForm.submit(function(event){
      event.preventDefault();

      console.log("Form is not sending")

      var thisForm = $(this)
      var actionEndpoint = thisForm.attr("action")
      var httpMethod = thisForm.attr("method")
      var fromData = thisForm.serialize()

      $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          dataType: 'json',
          beforeSend: function () {
            $("#modal-election").modal("show");
          },
          success: function (data) {
            $("#modal-election .modal-content").html(data.html_form);
          }
       });

    });
 });*/
