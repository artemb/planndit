/**
 * Created by Sekai Kagami on 13.01.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('vehicleService', function($http) {

            var vehicles;

            return {
                getVehicles: function() {
                    return vehicles;
                },

                loadVehicle: function() { //todo create vehicle service
                    var promise = $http.post(apiUrl + 'vehicle/');

                    promise.then(function(response) {
                        vehicles = response.data
                    });

                    return promise;
                }
            }
        })
})();