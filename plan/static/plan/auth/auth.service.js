/**
 * Created by Sekai Kagami on 02.02.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('authService', function($http, mainService) {
            return {
                login: function(username, password) {
                    var promise = $http.post(apiUrl + 'auth/login/', {
                        username: username,
                        password: password
                    });

                    return promise;
                },

                logout: function() {
                    var promise = $http.post(apiUrl + 'auth/logout/');

                    return promise;
                }
            }
        })
})();