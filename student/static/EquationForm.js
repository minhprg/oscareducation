var myDic = {};
function submit2(id){
    if( !(id in myDic)){
       myDic[id] = [];
    }
    var text = document.getElementById("text".concat(id.toString())).value;
    if(text != ""){
        myDic[id].push(text);
        listToAnswer(id);
        document.getElementById("text".concat(id.toString())).value = "";
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

function myInputHandler(event, id){
    	if(event.which == 13 | event.keyCode == 13) {
            event.preventDefault();
            event.stopImmediatePropagation();
            submit2(id);
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
    console.log(texteq1)
    console.log(texteq2)
    if(texteq1 != "" && texteq2 != ""){
        myDic[id].push([texteq1, texteq2]);
        listToAnswerSystem(id);
        document.getElementById("textEq2".concat(id.toString())).value = "";
        document.getElementById("textEq1".concat(id.toString())).value = "";
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
