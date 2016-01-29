/**
 * Created by Sekai Kagami on 24.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit') // todo DEPRICATED
        .factory('routeService_old', function($http, $filter) {
            var routes;

            return {
                getCurrentRoutes: function() {
                    return routes;
                },

                createRoute: function() {
                    var promise = $http.post(apiUrl + 'create_route');

                    return promise;
                },

                loadRoutes: function(date) {
                    date = $filter('date')(date, 'yyyy-MM-dd');
                    var promise = $http.post(apiUrl + 'route/', {date: date, a: 'a'});

                    promise.then(function(response) {
                        routes = response.data;
                    });


                    return promise;
                }
            }
        })
})();