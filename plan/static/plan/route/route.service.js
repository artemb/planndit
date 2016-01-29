/**
 * Created by Sekai Kagami on 24.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('routeService', function($http, $filter) {
            var routes;
            var route;

            return {
                getRoutes: function() {
                    return routes;
                },

                getCurrentRoute: function() {
                    return route;
                },

                getVehicles: function() {
                    return vehicles;
                },

                createRoute: function() {
                    var promise = $http.post(apiUrl + 'route/create');

                    return promise;
                },

                loadRoute: function(id) {
                    var promise = $http.post(apiUrl + 'route/' + id);

                    promise.then(function(response) {
                        route = response.data;
                    });

                    return promise;
                },

                loadRoutes: function(date) {
                    date = $filter('date')(date, 'yyyy-MM-dd');
                    var promise = $http.post(apiUrl + 'route/', {'date': date});

                    promise.then(function(response) {
                        routes = response.data;
                    });

                    return promise;
                },

                updateOrders: function(routeId, orders) {
                    var promise = $http.post(apiUrl + 'route/update_orders/', {
                        routeId: routeId,
                        orders: orders
                    });

                    return promise;
                },

                changeVehicle: function(routeId, vehicleId) {
                    var promise = $http.post(apiUrl + 'route/update_vehicle/', {
                        routeId: routeId,
                        vehicleId: vehicleId
                    });

                    return promise;
                },

                removeOrder: function(routeId, orderId) {
                    var promise = $http.post(apiUrl + 'route/remove_order', {
                        routeId: routeId,
                        orderId: orderId
                    });

                    return promise;
                },

                resequence: function(routeId) {
                    var promise = $http.post(apiUrl + 'route/resequence/', {
                        routeId: routeId
                    });

                    promise.then(function(response) {
                        route = response.data;
                    });

                    return promise;
                }
            }
        })
})();