
var xhr = new XMLHttpRequest();

//update the generation of the exercice id
//the problem right now is that the id doesn't change as the temple use ng-repeat.
//we need to find a way
function updateAutoGeneration(id){

    if(document.getElementById("typebox")){
        var typeBox = document.getElementById("typebox");
        var type = typeBox.options[typeBox.selectedIndex].value;
    }
    var idstring = id.toString()
    if(document.getElementById("vl".concat(id))){
        var varleft = document.getElementById("vl".concat(id)).checked;
    }
    if(document.getElementById("vr".concat(id))){
        var varright = document.getElementById("vr".concat(id)).checked;
    }
    if(document.getElementById("cmini".concat(id))){
        var coefmini = document.getElementById("cmini".concat(id)).value;
    }
    if(document.getElementById("cmaxi".concat(id))){
        var coefmaxi = document.getElementById("cmaxi".concat(id)).value;
    }
    if(document.getElementById("smini".concat(id))){
        var smini = document.getElementById("smini".concat(id)).value;
    }
    if(document.getElementById("smaxi".concat(id))){
        var smaxi = document.getElementById("smaxi".concat(id)).value;
    }
    if( document.getElementById("var".concat(id))){
        var varVar = document.getElementById("var".concat(id)).value;
    }
    if( document.getElementById("frac".concat(id))){
        var frac = document.getElementById("frac".concat(id)).checked;
    }
    if( document.getElementById("sint".concat(id))){
        var sint = document.getElementById("sint".concat(id)).checked;
    }
    if( document.getElementById("more".concat(id))){
        if(type == "algebraicSystem"){
            var more = document.getElementById("more".concat(id)).value;
        }
        else{
            var more = document.getElementById("more".concat(id)).checked;
        }
    }
    console.log(more);

   if(type == "algebraicSystem") {

        sendRequest(idstring, type+"/"+"0/0/"+coefmini+"/"+coefmaxi+"/"+smini+"/"+smaxi+"/"+varVar+"/"+frac+"/"+sint+"/"+more+"/");
   }
   else if (type == "algebraicExpression"){
       sendRequest(idstring, type+"/"+varleft+"/"+varright+"/"+coefmini+"/"+coefmaxi+"/"+smini+"/"+smaxi+"/"+varVar+"/"+frac+"/"+sint+"/"+more+"/");

   }
   else{
       sendRequest(idstring, type+"/"+varleft+"/"+varright+"/"+coefmini+"/"+coefmaxi+"/"+smini+"/"+smaxi+"/"+varVar+"/"+frac+"/"+sint+"/"+"0/");

   }

}
//send an html request to the web site.
function sendRequest(id, string){
    xhr.open('GET', "/professor/equationGeneration/"+encodeURIComponent(id.toString())+"/"+string,true);
    xhr.send(null);

    xhr.addEventListener("readystateechange", processRequest, false);
    xhr.onreadystatechange = processRequest;
}
//process the request
function processRequest(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        //var response = JSON.parse(xhr.responseText);
        spl = xhr.responseText.split(":");
        //the response is in form [id, type, equation]
        if(spl[1] == "algebraicSystem"){
            document.getElementById("generatedEquation1".concat(spl[0])).value = spl[2].split(";")[0];
            document.getElementById("generatedEquation2".concat(spl[0])).value = spl[2].split(";")[1];
            angular.element(document.getElementById("generatedEquation1".concat(spl[0]))).triggerHandler('change');
            angular.element(document.getElementById("generatedEquation2".concat(spl[0]))).triggerHandler('change');

        }
        else{
            document.getElementById("generatedEquation".concat(spl[0])).value = spl[2];
            angular.element(document.getElementById("generatedEquation".concat(spl[0]))).triggerHandler('change');

        }


    }
}
