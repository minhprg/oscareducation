
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
    verifResponse();
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

function verifResponse(){
  var exerciceToSend = {
    expression: $("#expression_"+question).html(),
    type: "Equation" ,
    solution: $("#step1").val() ,
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
    $("#hintstep1").val("ok").removeClass("alert-danger").addClass("alert-success");
    });

  request.fail(function(xhr) {

    $("#hintstep1").val("erreur").removeClass("alert-success").addClass("alert-danger");
    });

}
