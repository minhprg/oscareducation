function severalQuestionsController($scope, $window) {
    $scope.questions = [1];

    $scope.addMoreQuestion = function(number) {

        if ($scope.questions.length > 0) {
            var new_number = $scope.questions[$scope.questions.length - 1] + 1;
        } else {
            var new_number = 0;
        }

        for (var i = 0; i < number; ++i) {
            $scope.questions.push(new_number + i);
        }
    }

    $scope.removeQuestion = function(id) {
        if($scope.questions.length > 1) {
            $scope.questions.splice($scope.questions.length-1, 1);
        }
    }
}

