/**
 * Created by Sekai Kagami on 13.01.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('gisService', function($http, $filter) {
            return {
                geocode: function(address) {
                    var promise = $http.post(apiUrl + 'geocode/', {
                        address: address
                    });

                    promise.then(function(response) {
                        response.data;
                    });

                    return promise;
                }
            }
        })
})();