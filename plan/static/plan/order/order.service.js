/**
 * Created by Sekai Kagami on 27.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('orderService', function($http, $filter) {
            var order;

            return {
                getOrder: function() {
                    return order;
                },

                loadOrder: function(orderId) {
                    var promise = $http.get(apiUrl + 'order/' + orderId);

                    promise.then(function(response) {
                        order = response.data;
                    });

                    return promise;
                },

                updateOrder: function(orderId, order) {
                    var promise = $http.post(apiUrl + 'order/' + orderId, order);

                    return promise;
                }
            }
        })
})();