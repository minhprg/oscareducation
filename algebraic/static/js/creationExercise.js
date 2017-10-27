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
  //concaténation des deux coté plus signe
  $("#concat").click(function(){
    output=$("#leftSide").val()+$("#signe").val()+$("#rightSide").val();
    $("#solution").val(output);
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
