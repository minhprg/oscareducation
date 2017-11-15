var myDic = {};
function submit2(id){
    console.log(id);
   console.log(document.getElementById("text".concat(id.toString())).value)
    if( !(id in myDic)){
       myDic[id] = [];
    }
    myDic[id].push(document.getElementById("text".concat(id.toString())).value);
    console.log(myDic[id]);

    document.getElementById("pre".concat(id.toString())).innerHTML = myDic[id];
    document.getElementById(id).innerHTML = myDic[id];


}
function controller1($scope){
    $scope.submit2 = function(){

        console.log("yepaaaah")
    }
}
var equationApp = angular.module('submitExample', []);
equationApp.controller('EquationController', ['$scope', function($scope) {
    $scope.list = [];
    $scope.text = 'hello world';
    console.log("oui j'ai été run")
    $scope.submit2 = function() {
        if ($scope.text) {
          $scope.list.push(this.text);
          $scope.text = '';
        }
      };
    }]);
