var myDic = {};
function submit2(id){
    console.log(id);
    console.log(document.getElementById("ans".concat(id.toString())).value)
   console.log(document.getElementById("text".concat(id.toString())).value)
    if( !(id in myDic)){
       myDic[id] = [];
       myDic[id].push(document.getElementById("ans".concat(id.toString())).value);
    }
    var text = document.getElementById("text".concat(id.toString())).value;
    if(text != ""){
        myDic[id].push(text);
    }

    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    var txt = ""
    for (var i = 0 ; i < myDic[id].length; i++){
        txt=txt.concat(":").concat(myDic[id][i]);
    }
    console.log(txt);
    document.getElementById(id.toString()).value = txt;
    console.log(document.getElementById(id.toString()).value);


}
function pushFirstEquation(id,equation){
    if( !(id in myDic)){
       myDic[id] = [];
    }
    myDic[id].push(equation);
    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    document.getElementById(id.toString()).innerHTML = myDic[id];

}

