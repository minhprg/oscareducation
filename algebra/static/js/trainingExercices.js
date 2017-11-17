
  var question = 1;
  var nbrQuestion = 0;

$(document).ready(function(){
  $("#clear").click(function(){
    $(".form-control").val("");
  });
  $("#previous").click(function(){
    if (question>1) chargeQuestion(question-1);
  });
  $("#next").click(function(){
    if (question<nbrQuestion) chargeQuestion(question+1);
  });

  $("#check").click(function(){
    if ($("#step1").val()!="") verifResponse(1);
    if ($("#step2").val()!="") verifResponse(2);
    if ($("#step3").val()!="") verifResponse(3);
    if ($("#step4").val()!="") verifResponse(4);
  });

  chargeQuestion(1);

  var nbrRows = Math.ceil(nbrQuestion/2);
  var html = "";
  for (var i = 0; i < nbrRows; i++) {
    html += "<div class='row'>"+
           "<div class='align-self-center col-md-6 p-1'>"+
              "<a href='#' class='btn btn-primary btn-block' onclick='chargeQuestion("+(i+1+(1*i))+")'>Q "+(i+1+(1*i))+"</a>"+
           "</div>"+
           "<div class='align-self-center col-md-6 p-1'>"+
              "<a href='#' class='btn btn-primary btn-block' onclick='chargeQuestion("+(i+2+(1*i))+")'>Q "+(i+2+(1*i))+"</a>"+
           "</div></div>";
  }
  $("#clickQuestions").html(html);


});


function chargeQuestion (num){
  question = num;
  $("#question_title").html("Question "+question+" :");

  var i = 0;
  $(".equation").each(function(){
    i++;
    $("#"+this.id).attr("id", "expression_"+i);
    if (i!=question){
      $("#"+this.id).addClass("hide");
    }
    else {$("#"+this.id).removeClass("hide");}
  });


  var i = 0;
  $(".equation_type").each(function(){
    i++;
    $("#"+this.id).attr("id", "type_"+i);
    if (i!=question){
      $("#"+this.id).addClass("hide");
    }
    else {$("#"+this.id).removeClass("hide");}
  });
  nbrQuestion = i;

  var i = 0;
  $(".equation_level").each(function(){
    i++;
    $("#"+this.id).attr("id", "level_"+i);
    if (i!=question){
      $("#"+this.id).addClass("hide");
    }
    else {$("#"+this.id).removeClass("hide");}
  });
}

function verifResponse(step){
  var exerciceToSend = {
    expression: $("#expression_"+question).html(),
    type: "Equation" ,
    solution: $("#step"+step).val() ,
    level: "1",
    };

  var request=$.ajax({
    url: '/algebra/student/training_session',
    type: 'POST',
    data: JSON.stringify(exerciceToSend),
    contentType: 'application/json',
    dataType: 'json',
    });

  request.done(function(data) {
    // message success
    $("#hintstep"+step).val("ok").removeClass("alert-danger").addClass("alert-success");
    });

  request.fail(function(xhr) {

    $("#hintstep"+step).val("erreur").removeClass("alert-success").addClass("alert-danger");
    });

}
