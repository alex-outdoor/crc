app = angular.module("form", ["ngCookies"]);
app.controller("FormController", [
  "$scope",
  "$http",
  "$cookies",
  function($scope, $http, $cookies) {
    $scope.load = function() {
      // Actions when loading the form
      $scope.qte = [];
      // By default, 5000 words
      $("#translation_words").val("5000");
      update();
      get_clients();
    };

    $scope.show_deliverables = function() {
      // Show the deliverables table
      $("#deliverables_table").removeClass("hidden");
    };

    $scope.add_respondent = function() {
      $scope.qte.push($scope.qte.length + 1);
    };

    $scope.remove_respondent = function() {
      if ($scope.qte.length > 0) {
        $scope.qte.pop();
      }
    };

    var update = function() {
      val = $("#translation_words").val() * 0.3;
      // For the UI
      $("#translation_total").val(val);
      // For django hidden field because disabled field in UI
      $("#translation_total2").val(val);
    };
    
    $("#translation_words").change(update);

    var get_clients = function() {
      url = "http://" + location.host + "/api/clients/";
      // API call
      $http.get(url).success(function(data, status, headers, config) {
        $scope.clients = [];
        for (var i = 0; i < data.length; i++) {
          $scope.clients.push(data[i]);
        }
      });
    };
  }
]);
