'use strict';


angular.module("linkeddeed", []).controller("JobsController", ['$scope', function ($scope) {
    $scope.jobs = [
        {url: 'https://www.github.com'
            },
        {url: 'https://www.github.com'
            }
    ];
}]);