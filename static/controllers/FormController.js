app = angular.module("form", ["ngCookies"]);
app.controller("FormController", [
  "$scope",
  "$http",
  "$cookies",
  function($scope, $http, $cookies) {
    $scope.show_deliv = false;
    $scope.show_facil = false;
    $scope.show_mod = false;

    $scope.load = function() {
      // Actions when loading the form

      // Editing an existing BID
      // pathname is /crc/new_bid/bid_id when editing
      var url_path = location.pathname.split("/");
      var bid_id = url_path[url_path.length - 1];
      if (bid_id != "") {
        console.log("editing bid", bid_id);
        // API call
        var url = "http://" + location.host + "/api/bid/" + bid_id;
        $http.get(url).success(function(data, status, headers, config) {
          // For Django procession view
          $("#translation_total2").val(data["translation_cost"]);

          var respondents = data.respondents;
          $scope.qte = [];
          for (var i = 0; i < respondents.length; i++) {
            var index = i + 1;
            // Open x windows for respondents group details
            $scope.qte.push(index);
          }
          // (delay because id are generated based on $index in ng-repeat)
          setTimeout(function() {
            for (var i = 0; i < respondents.length; i++) {
              // Fill in the infos
              // Respondent group
              $("#nbr_respondent_@".replace("@", i)).val(respondents[i].nbr_respondent);
              $("#nbr_over_recruitment_@".replace("@", i)).val(respondents[i].over_recruitment);
              $("#type_respondent_@".replace("@", i)).val(respondents[i].type_respondent);
              $("#city_@".replace("@", i)).val(respondents[i].city);
              $("#incentive_@".replace("@", i)).val(respondents[i].incentive);
              $("#duration_@".replace("@", i)).val(respondents[i].methodologies[0].duration);
              $("#recruitment_cost_@".replace("@", i)).val(respondents[i].nbr_respondent);
              $("#language_@".replace("@", i)).val(respondents[i].language);
              $("#notes_respondent_@".replace("@", i)).val(respondents[i].notes);

              // Methodology
              var methods = [
                "olbb",
                "online_focus_group",
                "ethnographic_interview",
                "web_tdi",
                "idi",
                "focus_group",
                "tdi",
                "taste_test"
              ];
              if (methods.indexOf(respondents[i].methodologies[0].name) >= 0) {
                $(
                  "[name=radio_@][value=&]"
                    .replace("@", i)
                    .replace("&", respondents[i].methodologies[0].name)
                ).prop("checked", true);
              } else {
                $("[name=radio_@][value=other_test]".replace("@", i)).prop("checked", true);
                $("#other_test_name_@".replace("@", i)).val(respondents[i].methodologies[0].name);
              }
            }
          }, 100);

          // Deliverables
          var existing_deliverables = [
            "english_to_english",
            "french_to_english",
            "content_analysis",
            "topline_report",
            "full_report",
            "summary_report",
            "discussion_guide_design",
            "screener_design"
          ];
          var deliverables = data.deliverables;
          if (deliverables.length > 0) {
            $("#deliverables_table").show();
            for (var j = 0; j < deliverables.length; j++) {
              $("[name=@_cost]".replace("@", deliverables[j].name)).val(deliverables[j].unit_cost);
              $("[name=@_qty]".replace("@", deliverables[j].name)).val(deliverables[j].quantity);
              $("[name=@_duration]".replace("@", deliverables[j].name)).val(
                deliverables[j].duration
              );
              if (existing_deliverables.indexOf(deliverables[j].name) < 0) {
                // This is for other deliverable
                $("[name=other_deliverable]").val(deliverables[j].name);
                $("[name=other_deliverable_qty]").val(deliverables[j].quantity);
                $("[name=other_deliverable_duration]").val(deliverables[j].duration);
                $("[name=other_deliverable_cost]").val(deliverables[j].unit_cost);
              }
            }
            $scope.notes_deliverables = deliverables[0].notes;
          }
        });
        get_clients();
      } else {
        // This is a new BID
        // Creation a new BID
        $scope.qte = [];
        // By default, 5000 words
        $("#translation_words").val("5000");
        update();
        get_clients();
      }
    };

    $scope.show_deliverables = function() {
      // Show the deliverables table
      $scope.show_deliv = $scope.show_deliv ? false : true;
    };

    $scope.show_facility = function() {
      // Show the facility table
      $scope.show_facil = $scope.show_facil ? false : true;
    };

    $scope.show_moderation = function() {
      // Show the moderation table
      $scope.show_mod = $scope.show_mod ? false : true;
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
