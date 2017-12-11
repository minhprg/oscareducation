//used to store the lists used for answering the questions
var myDic = {};
var xhr = new XMLHttpRequest();

//process the http answers
function processRequest(e){
    console.log("test");
    if (xhr.readyState == 4 && xhr.status == 200){
        //var response = JSON.parse(xhr.responseText);
        console.log(xhr.responseText)
        var lis = xhr.responseText.split(":")
        //the answer is in form Valid:type:id:step
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
//send the http request
function handlePythonCall(equation, id, type){


    xhr.open('GET', "../../equationVerification/"+encodeURIComponent(id.toString())+"/"+encodeURIComponent(type.toString())+"/"+encodeURIComponent(equation.toString().replace(" ","").replace("/","&")), true);
    xhr.send(null);

    xhr.addEventListener("readystateechange", processRequest, false);
    xhr.onreadystatechange = processRequest;

}
//submit
function submit2(id, type){
    if( !(id in myDic)){
       myDic[id] = [];
    }
    var text = document.getElementById("text".concat(id.toString())).value;
    if(text != ""){
        handlePythonCall(text, id, type)
    }
    else {
        document.getElementById("text".concat(id.toString())).focus();
    }


}
//translate the lists of step to string to let the user preview.
function listToAnswer(id){
    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    var txt = ""
    for (var i = 0 ; i < myDic[id].length; i++){
        txt=txt.concat(":").concat(myDic[id][i]);
    }
    document.getElementById(id.toString()).value = txt;
}
//clear the last step
function clearLastStep(id){
    if( id in myDic){
       if(myDic[id].length != 0) {
           myDic[id].pop();
           listToAnswer(id);
       }
    }
}
//clear the last step for system
function clearLastStepSystem(id){
    if( id in myDic){
       if(myDic[id].length != 0) {
           myDic[id].pop();
           listToAnswerSystem(id);
       }
    }
}

//handle input. Used to prevent submitting the form when hitting enter
function myInputHandler(event, id, type){
    	if(event.which == 13 | event.keyCode == 13) {
            event.preventDefault();
            event.stopImmediatePropagation();
            submit2(id, type);
            return false;
        }
        return true;
}
//handle input. Used to prevent submitting the form when hitting enter and to switch the focus
function myInputHandlerSystem(event, id){
    	if(event.which == 13 | event.keyCode == 13) {
            event.preventDefault();
            event.stopImmediatePropagation();
            submitSystem(id);
            return false;
        }
        return true;
}
//submit system
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
//used to display the answer to the user
function listToAnswerSystem(id){
    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    var txt = ""
    for (var i = 0 ; i < myDic[id].length; i++){
        txt=txt.concat(":").concat(myDic[id][i][0].concat(";").concat(myDic[id][i][1]));
    }
    document.getElementById(id.toString()).value = txt;
}
