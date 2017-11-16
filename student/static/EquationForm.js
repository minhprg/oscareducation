var myDic = {};
function submit2(id){
    if( !(id in myDic)){
       myDic[id] = [];
       //myDic[id].push(document.getElementById("ans".concat(id.toString())).value);
    }
    var text = document.getElementById("text".concat(id.toString())).value;
    if(text != ""){
        myDic[id].push(text);
    }
    listToAnswer(id);
    document.getElementById("ans".concat(id.toString())).value = "";


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
function pushFirstEquation(id,equation){
    if( !(id in myDic)){
       myDic[id] = [];
    }
    myDic[id].push(equation);
    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    document.getElementById(id.toString()).innerHTML = myDic[id];

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
