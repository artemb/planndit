/**
 * Created by Sekai Kagami on 24.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('OrderController',[
            '$scope', 'orderService', '$stateParams', '$state', 'gisService',
            function($scope, orderService, $stateParams, $state, gisService) {
                var self = this;
                $scope.loading = false;

                orderService.loadOrder($stateParams.orderId).then(function() {
                    $scope.order = orderService.getOrder();
                    $scope.$broadcast('showOrder', $scope.order);
                });

                $scope.update = function() {
                    orderService.updateOrder($stateParams.orderId, $scope.order).then(function() {
                        $state.go('route', {id: $stateParams.routeId})
                    })
                };

                $scope.back = function() {
                    $state.go('route', {id: $stateParams.routeId})
                };

                $scope.geocode = function(address) {
                    $scope.loading = true;
                    if (self.timeout) {
                        clearTimeout(self.timeout);
                    }
                    self.timeout = setTimeout(function() {
                        gisService.geocode(address).then(function(response) {
                            $scope.order.location = response.data;
                            $scope.$broadcast('showOrder', $scope.order);
                            $scope.loading = false;
                            delete self.timeout;
                        })
                    }, 1000);

                };

            }])
})();