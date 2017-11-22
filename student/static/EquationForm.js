var myDic = {};
var xhr = new XMLHttpRequest();

function processRequest(e){
    console.log("test");
    if (xhr.readyState == 4 && xhr.status == 200){
        //var response = JSON.parse(xhr.responseText);
        console.log(xhr.responseText)
        var lis = xhr.responseText.split(":")
        if(lis[0] == "1"){
            if(lis[1] == "algebraicSystem"){
                if(myDic[lis[2]].length >= 10){
                    alert("Vous avez soumis trop d'étapes !")
                }
                else {
                    var spl = lis[3].split(";");
                    myDic[lis[2]].push([spl[0], spl[1]]);
                    listToAnswerSystem(lis[2]);
                    document.getElementById("textEq2".concat(lis[2].toString())).value = "";
                    document.getElementById("textEq1".concat(lis[2].toString())).value = "";
                }
            }
            else{
                if(myDic[lis[2]].length >= 10){
                    alert("Vous avez soumis trop d'étapes !")
                }
                else {
                    myDic[lis[2]].push(lis[3]);
                    listToAnswer(lis[2]);
                    document.getElementById("text".concat(lis[2].toString())).value = "";
                }
            }

        }
        else{
            alert(lis[1]);
        }


    }
}
function handlePythonCall(equation, id, type){


    xhr.open('GET', "../../equationVerification/"+encodeURIComponent(id.toString())+"/"+encodeURIComponent(type.toString())+"/"+encodeURIComponent(equation.toString().replace(" ","").replace("/","&")), true);
    xhr.send(null);

    xhr.addEventListener("readystateechange", processRequest, false);
    xhr.onreadystatechange = processRequest;

}
function submit2(id, type){
    if( !(id in myDic)){
       myDic[id] = [];
    }
    var text = document.getElementById("text".concat(id.toString())).value;
    if(text != ""){
        //myDic[id].push(text);
        //listToAnswer(id);
        handlePythonCall(text, id, type)
        //document.getElementById("text".concat(id.toString())).value = "";
    }
    else {
        document.getElementById("text".concat(id.toString())).focus();
    }


}
function listToAnswer(id){
    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    var txt = ""
    for (var i = 0 ; i < myDic[id].length; i++){
        txt=txt.concat(":").concat(myDic[id][i]);
    }
    document.getElementById(id.toString()).value = txt;
}
function clearLastStep(id){
    if( id in myDic){
       if(myDic[id].length != 0) {
           myDic[id].pop();
           listToAnswer(id);
       }
    }
}
function clearLastStepSystem(id){
    if( id in myDic){
       if(myDic[id].length != 0) {
           myDic[id].pop();
           listToAnswerSystem(id);
       }
    }
}

function myInputHandler(event, id, type){
    	if(event.which == 13 | event.keyCode == 13) {
            event.preventDefault();
            event.stopImmediatePropagation();
            submit2(id, type);
            return false;
        }
        return true;
}
function myInputHandlerSystem(event, id){
    	if(event.which == 13 | event.keyCode == 13) {
            event.preventDefault();
            event.stopImmediatePropagation();
            submitSystem(id);
            return false;
        }
        return true;
}
function submitSystem(id){
    if( !(id in myDic)){
       myDic[id] = [];
       //myDic[id].push(document.getElementById("ans".concat(id.toString())).value);
    }
    var texteq1 = document.getElementById("textEq1".concat(id.toString())).value;
    var texteq2 = document.getElementById("textEq2".concat(id.toString())).value;

    if(texteq1 != "" && texteq2 != "" && texteq1 != null && texteq2 != null ){
        //myDic[id].push([texteq1, texteq2]);
        //listToAnswerSystem(id);
        handlePythonCall(texteq1.concat(";").concat(texteq2),id,"algebraicSystem");
        //document.getElementById("textEq2".concat(id.toString())).value = "";
        //document.getElementById("textEq1".concat(id.toString())).value = "";
    } else if( texteq1 == "" || texteq1 == null){

        console.log("error");
        document.getElementById("textEq1".concat(id.toString())).focus();
    } else {
        console.log("error");
        document.getElementById("textEq2".concat(id.toString())).focus();

    }
}

function listToAnswerSystem(id){
    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    var txt = ""
    for (var i = 0 ; i < myDic[id].length; i++){
        txt=txt.concat(":").concat(myDic[id][i][0].concat(";").concat(myDic[id][i][1]));
    }
    document.getElementById(id.toString()).value = txt;
}
