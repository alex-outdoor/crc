app = angular.module("auth", ["ngCookies"]);
app.controller("Authentification", [
  "$scope",
  "$http",
  "$cookies",
  function($scope, $http, $cookies) {
    $scope.init = function() {
      // Actions when loading the form
      $("h2").addClass("control-label register_title");
      $("label").addClass("control-label required");
      //$("input").addClass("form-control");
      $("button").addClass("btn btn-primary register-button");
    };
  }
]);
