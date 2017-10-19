app = angular.module('form', ['ngCookies']);
app.controller('FormController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {

  $scope.load = function(){
    // Actions when loading the form
    $scope.qte = [];
    // By default, 5000 words
    $('#translation_words').val('5000');
    update()
  }

  $scope.show_deliverables = function(){
    // Show the deliverables table
    $('#deliverables_table').removeClass('hidden')
  }

  $scope.add_respondent = function(){
    $scope.qte.push($scope.qte.length+1)
  }
  
  $scope.remove_respondent = function(){
    if($scope.qte.length > 0){
      $scope.qte.pop()
    }
    
  }
  
  var update = function(){
    $('#translation_total').val($('#translation_words').val() * 0.3);
  }
  $('#translation_words').change(update)
  

}]);
