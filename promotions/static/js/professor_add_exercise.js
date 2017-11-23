
var xhr = new XMLHttpRequest();
var maxId = 0

function updateAutoGeneration(id){
    console.log(typeof(id));
    console.log(id);
    var typeBox = document.getElementById("typebox");
    var type = typeBox.options[typeBox.selectedIndex].value;
    var idstring = id.toString()
    var varleft = document.getElementById("vl".concat(id)).checked;
    var varright = document.getElementById("vr".concat(id)).checked;
    var coefmini = document.getElementById("cmini".concat(id)).value;
    var coefmaxi = document.getElementById("cmaxi".concat(id)).value;
    var smini = document.getElementById("smini".concat(id)).value;
    var smaxi = document.getElementById("smaxi".concat(id)).value;
    var varVar = document.getElementById("var".concat(id)).value;
    var frac = document.getElementById("frac".concat(id)).checked;
    var sint = document.getElementById("sint".concat(id)).checked;
    console.log(idstring)
    console.log(varleft)
    console.log(varright)
    console.log(coefmini)
    console.log(coefmaxi)
    console.log(smini)
    console.log(smaxi)
    console.log(varVar)
    console.log(frac)
    console.log(sint)

   if(type == "algebraicSystem") {

        sendRequest(idstring, type+"/"+varleft+"/"+varright+"/"+coefmini+"/"+coefmaxi+"/"+smini+"/"+smaxi+"/"+varVar+"/"+frac+"/"+sint+"/");
   }
   else if (type == "algebraicExpression"){
       sendRequest(idstring, type+"/"+varleft+"/"+varright+"/"+coefmini+"/"+coefmaxi+"/"+smini+"/"+smaxi+"/"+varVar+"/"+frac+"/"+sint+"/");

   }
   else{
       sendRequest(idstring, type+"/"+varleft+"/"+varright+"/"+coefmini+"/"+coefmaxi+"/"+smini+"/"+smaxi+"/"+varVar+"/"+frac+"/"+sint+"/");

   }

}
function sendRequest(id, string){
    xhr.open('GET', "/professor/equationGeneration/"+encodeURIComponent(id.toString())+"/"+string,true);
    xhr.send(null);

    xhr.addEventListener("readystateechange", processRequest, false);
    xhr.onreadystatechange = processRequest;
}
function processRequest(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        //var response = JSON.parse(xhr.responseText);
        spl = xhr.responseText.split(":");
        document.getElementById("generatedEquation".concat(spl[0])).value = spl[1];
        angular.element(document.getElementById("generatedEquation".concat(spl[0]))).triggerHandler('change');


    }
}
