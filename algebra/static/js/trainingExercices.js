
  var question = 1;
  var nbrQuestion = 0;
  var nbrCorrectAnswers = 0;

$(document).ready(function(){
  $("#clear").click(function(){
    clear();
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
              "<a id='Q_"+(i+1+(1*i))+"' class='btn btn-primary btn-block' onclick='chargeQuestion("+(i+1+(1*i))+")'>Q "+(i+1+(1*i))+"</a>"+
           "</div>";
    if ((nbrQuestion%2)==1 && i==(nbrRows-1)){
        html+="";
      }
    else {
      html+="<div class='align-self-center col-md-6 p-1'>"+
          "<a id='Q_"+(i+2+(1*i))+"' class='btn btn-primary btn-block' onclick='chargeQuestion("+(i+2+(1*i))+")'>Q "+(i+2+(1*i))+"</a>"+
       "</div>";
     }
    html+=  "</div>";
  }
  $("#clickQuestions").html(html);


});


function chargeQuestion (num){
  question = num;
  clear();
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
      if (data.message == "Ok-solution"){
         if ($("#Q_"+question).hasClass('btn-primary')){
            nbrCorrectAnswers++;
            $("#Q_"+question).removeClass("btn-primary").addClass("alert-success");
            $("#success-progress").html("Success : "+nbrCorrectAnswers+"/"+nbrQuestion);
            $("#question-progress").css("width", Math.ceil((nbrCorrectAnswers/nbrQuestion)*100)+"%");
            $("#question-progress").html(Math.ceil((nbrCorrectAnswers/nbrQuestion)*100)+"%");
         }
      }
    });

  request.fail(function(xhr) {

    $("#hintstep"+step).val("erreur").removeClass("alert-success").addClass("alert-danger");
    });

}

function clear(){
  $(".form-control").val("");
  $("#hintstep1").val("").removeClass("alert-danger").removeClass("alert-success");
  $("#hintstep2").val("").removeClass("alert-danger").removeClass("alert-success");
  $("#hintstep3").val("").removeClass("alert-danger").removeClass("alert-success");
  $("#hintstep4").val("").removeClass("alert-danger").removeClass("alert-success");
}
