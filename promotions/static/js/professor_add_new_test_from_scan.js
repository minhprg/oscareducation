function add_test_from_scanController($scope, $window, $http) {
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
 $scope.stages = [];

    $scope.addSkillToTest = function(stage_id) {


        if ($scope.stages[stage_id].length == 0)
            return;

        var skill = $scope["stage" + stage_id + "SelectedSkill"];
        $scope.toTestSkills.push(skill);

        var toRemoveIndex;

        for (var index = 0; index < $scope.stages[stage_id].length; index++) {
            if ($scope.stages[stage_id][index].code == $scope["stage" + stage_id + "SelectedSkill"]) {
                toRemoveIndex = index;
            }
        }

        $scope.stages[stage_id].splice(toRemoveIndex, 1);

        if ($scope.stages[stage_id].length > 0) {
            $scope["stage" + stage_id + "SelectedSkill"] = $scope.stages[stage_id][0].code;
        } else {
            $scope["stage" + stage_id + "SelectedSkill"] = "";
            $("#addSkillToTestButtonForStage" + stage_id).addClass("disabled");
        }
        $("#skills-scan").val($scope.toTestSkills );
        $("#" + skill).hide();
    }

       update_test_list = function () {
        $http.get("/professor/lesson_tests_and_skills/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.stages = data.stages;
                $scope.toTestSkills = [];

                for (i in $scope.stages) {
                    $scope["stage" + i + "SelectedSkill"] = $scope.stages[i][0].code;
                }
           })
    }

    update_test_list();

    $scope.removeSkill = function(skill) {
        $scope.toTestSkills.splice($scope.toTestSkills.indexOf(skill), 1);
        $("#skills-scan").val($scope.toTestSkills );
        $("#" + skill).show();
    }

}