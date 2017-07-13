"use strict";
angular.module("smarthouseApp", ["ngAnimate", "ngAria", "ngCookies", "ngMessages", "ngResource", "ngRoute", "ngSanitize", "ngTouch"])
  .config(["$routeProvider", function(a) {
    a.when("/", {
      templateUrl: "views/main.html",
      controller: "MainCtrl",
      controllerAs: "main"
    })
    .when("/live-stream", {
      templateUrl: "views/live-stream.html",
      controller: "LiveStreamCtrl"
    })
    .when("/photos", {
      templateUrl: "views/photos.html",
      controller: "PhotosCtrl"
    })
    .when("/security", {
      templateUrl: "views/security.html",
      controller: "SecurityCtrl"
    })
    .otherwise({
      redirectTo: "/"
    })
  }]);

angular.module("smarthouseApp")
.controller("BaseController", ["$scope", "$location", function(a, b) {
  a.isActive = function(a) {
    return a === b.url()
  }
}]);

angular.module("smarthouseApp")
.controller("MainCtrl", function() {
  this.awesomeThings = ["HTML5 Boilerplate", "AngularJS", "Karma"]
});

angular.module("smarthouseApp")
.controller("LiveStreamCtrl", ["$scope", function(a) {
  a.streamStarted = !1;
  var b = "http://admin@" + window.location.hostname + ":81/video.cgi";
  a.startStream = function() {
    a.streamStarted || (a.streamStarted = !0, $("#video-stream")
        .attr("src", b))
  }
}]);

angular.module("smarthouseApp")
.controller("SecurityCtrl", ["$http", "$interval", "$scope", function($http, $interval, $scope) {
  $scope.streamStarted = !1;
  $scope.faceRecognitionOutput = "Processing...";

  var b = "http://admin@" + window.location.hostname + ":81/video.cgi";
  $scope.startStream = function() {
    $scope.streamStarted || ($scope.streamStarted = !0, $("#video-stream")
        .attr("src", b))
  }

  var ticker = $interval(function() {
    var host = window.location.hostname || "192.168.1.1";
    var url = "http://" + host + ":8011/snap";
    $http.get(url)
      .then(function(response) {
        $scope.faceRecognitionOutput = response.data;
      }, function(response) {
        $scope.faceRecognitionOutput = response.data || 'Request failed';
      });
  }, 2000);

  $scope.$on('$destroy', function() {
    $interval.cancel(ticker);
  });
}]);

angular.module("smarthouseApp")
.controller("PhotosCtrl", ["$scope", "$http", "$interval", function(a, b, c) {
  a.photos = [];
  var d = "http://" + window.location.hostname + ":8010",
  e = 6e4,
  f = null,
  g = function() {
    b.get(d)
      .then(function(b) {
        a.photos = b.data
      })
  };
  g(), f = c(g, e)
}]);
