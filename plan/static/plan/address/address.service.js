/**
 * Created by Sekai Kagami on 24.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('addressService', function($http, $filter) {

            return {
                import: function(data, routeId) {
                    var promise = $http.post(apiUrl + 'import/', {
                        orders: data,
                        routeId: routeId
                    }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    return promise;
                }
            }
        })
})();