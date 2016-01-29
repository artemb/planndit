/**
 * Created by Sekai Kagami on 24.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('RouteListController',
            function($scope, routeService, $state) {
                $scope.date = new Date();
                var loadRoutes = function() {
                    routeService.loadRoutes($scope.date).then(function() {
                        $scope.routes = routeService.getRoutes();
                    });
                };

                $scope.createRoute = function() {
                    routeService.createRoute($scope.date).then(function(response) {
                        $scope.routes.push(response.data);
                    })
                };

                $scope.edit = function(id) {
                    $state.go('route', {id: id});
                };

                //datepicker
                $scope.status = {
                    opened: false
                };
                $scope.open = function($event) {
                    $scope.status.opened = true;
                };
                $scope.setDate = function(year, month, day) {
                    $scope.date = new Date(year, month, day);
                };
                $scope.$watch('date', function() {
                    loadRoutes();
                })
            })
})();