$(document).ready(function(){
  //gestion de l'aspect "radio" des boutons
  $(".radio-side").click(function(){
    $(".radio-side").removeClass("btn-primary");
    $(this).addClass("btn-primary");
  });
  //appels pour écrire
  $("#addTermWithVariable").click(function(){
    writeSide("#termWithVariable");
  });
  $("#addTermWithoutVariable").click(function(){
    writeSide("#termWithoutVariable");
  });
  $("#addOperator").click(function(){
    writeSide("#operator");
  });
  //gestion du submit form
  $('form').submit(function(event) {
    var exerciceToSend,exerciceType;

    switch ($("#signe").val()) {
      case "=":
      exerciceType = "Equation";
      break;
      case "<",">":
      exerciceType = "Inequation";
      break;
    }

    var exerciceToSend = {
      expression: $("#leftSide").val()+$("#signe").val()+$("#rightSide").val(),
      type: "Equation" ,
      solution: $("#solution").val() ,
      level: $("#exercice_level").val(),
    };

    var request=$.ajax({
      url: '/algebra/exercice/creation',
      type: 'POST',
      data: JSON.stringify(exerciceToSend),
      contentType: 'application/json',
      dataType: 'json',
    });

    request.done(function(data) {
      // message success
      $("#status").html(`<div class="alert alert-success" role="alert">
      La solution est `+data.message+`
      </div>`)

      console.log("La solution est "+data.message);
    });

    request.fail(function(xhr) {
      //message fail
      console.log("Erreur "+xhr.status+" : "+xhr.responseJSON.message);
      $("#status").html(`<div class="alert alert-danger" role="alert">
      Erreur `+xhr.status+" : "+xhr.responseJSON.message+`
      </div>`)
    });

    // stop action submit
    event.preventDefault();
  });
});

  //gestion de l'ecriture d'un coté ou d'un autre
  function writeSide(input){
    output=$(input).val();
    if(input=="#termWithVariable"){
      output+=$("#var").val();
    }
    $("input"+input).val("");
    if($("#leftButton").hasClass("btn-primary")){
      output=$("#leftSide").val()+output;
      $("#leftSide").val(output);
    }
    if($("#rightButton").hasClass("btn-primary")){
      output=$("#rightSide").val()+output;
      $("#rightSide").val(output);
    }
  }
