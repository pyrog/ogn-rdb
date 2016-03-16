var ognrdbApp = angular.module('ognrdbApp',[
  'ngRoute',
  'ognrdbControllers'
]);

ognrdbApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/receivers', {
        templateUrl: 'partials/receiver-list.html',
        controller: 'ReceiverListCtrl'
      }).
      otherwise({
        redirectTo: '/receivers'
      });
  }]);
