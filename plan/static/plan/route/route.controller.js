/**
 * Created by Sekai Kagami on 24.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('RouteController',[
            '$scope', 'routeService', '$stateParams', '$state', 'vehicleService',
            function($scope, routeService, $stateParams, $state, vehicleService) {

                vehicleService.loadVehicle().then(function() {
                    $scope.vehicles = vehicleService.getVehicles();
                });

                routeService.loadRoute($stateParams.id)
                    .then(function() {
                        $scope.route = routeService.getCurrentRoute();
                        $scope.$broadcast('routeUpdate');
                    });
                $scope.addAddress = function() {
                    $state.go('addAddresses', {id: $stateParams.id});
                };

                $scope.edit = function(id) {
                    $state.go('orderEdit', {
                        routeId: $stateParams.id,
                        orderId: id
                    });
                };

                $scope.select = function(vehicle) {
                    routeService.changeVehicle($stateParams.id, vehicle.id).then(function(response) {
                        if (response.data.success) {
                            $scope.route.vehicle = vehicle;
                        }
                    })
                };

                $scope.remove = function(order) {
                    routeService.removeOrder($stateParams.id, order.id).then(function(response) {
                        if (response.data.success) {
                            var index = $scope.route.orders.indexOf(order);
                            if (index >= 0) {
                                $scope.route.orders.splice(index, 1);
                                for (var i = 0; i < $scope.route.orders.length; i++) {
                                    $scope.route.orders[i].order = i;
                                }
                            } else {
                                index = $scope.route.invalid_orders.indexOf(order);
                                if (index >= 0) {
                                    $scope.route.invalid_orders.splice(index, 1);
                                }
                            }
                        }
                    })
                };

                $scope.resequence = function() {
                    routeService.resequence($stateParams.id).then(function() {
                        $scope.route = routeService.getCurrentRoute()
                        $scope.$broadcast('routeUpdate');
                    })
                };

                $scope.sortableOptions = {
                    handle: '.handler',
                    items: ".sortable",
                    axis: 'y',
                    helper: function(e, ui) {
                        ui.children().each(function() {
                            $(this).width($(this).width());
                        });
                        return ui;
                    },
                    start: function(event, ui) {
                        var start_pos = ui.item.index();
                        ui.item.data('start_pos', start_pos);
                    },
                    stop: function(e, ui) {
                        ui.item.children().each(function() {
                            $(this).width('');
                        });
                        if (this.isUpdate) {
                            var orders = {};
                            for (var i = 0; i < $scope.route.orders.length; i++) {
                                $scope.route.orders[i].order = i;
                                orders[$scope.route.orders[i].id] = $scope.route.orders[i].order;
                            }
                            routeService.updateOrders($stateParams.id, orders);
                        }
                    },
                    update: function(e, ui) {
                        this.isUpdate = true;
                    }
                };

                //datepicker
                $scope.status = {
                    opened: false
                };
                $scope.open = function() {
                    $scope.status.opened = true;
                };
                $scope.setDate = function(year, month, day) {
                    $scope.date = new Date(year, month, day);
                };
                $scope.$watch('date', function() {
                    //save date
                })
            }])
})();