$(document).ready(function(){

  var question = 1;

  $("#clear").click(function(){
    $(".form-control").val("");
  });

  $("#question_title").html("Question "+question+" :");

  var i = 0;
  $(".equation").each(function(){
    i++;
    $("#"+this.id).attr("id", "expression_"+i);
    if (i!=question){
      $("#"+this.id).css("display","none");
    }
  });


  var i = 0;
  $(".equation_type").each(function(){
    i++;
    $("#"+this.id).attr("id", "type_"+i);
    if (i!=question){
      $("#"+this.id).css("display","none");
    }
  });

  var i = 0;
  $(".equation_level").each(function(){
    i++;
    $("#"+this.id).attr("id", "level_"+i);
    if (i!=question){
      $("#"+this.id).css("display","none");
    }
  });


});
