app = angular.module("clientListing", ["ngCookies"]);
app.controller("ClientListing", [
  "$scope",
  "$http",
  "$cookies",
  function($scope, $http, $cookies) {
    // Init variables
    $scope.sortType = "created_date";
    $scope.sortReverse = true;

    $scope.init = function() {
      url = "http://" + location.host + "/api/clients/";
      
      $scope.base_url = "http://" + location.host;
      // API call
      $http.get(url).success(function(data, status, headers, config) {
        $scope.data_list = [];
        for (var i = 0; i < data.length; i++) {
          $scope.data_list.push(data[i]);
        }
      });
    };
  }
]);
