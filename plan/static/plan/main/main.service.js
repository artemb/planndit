/**
 * Created by Sekai Kagami on 02.02.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('mainService', function($http) {
            var currentUser = '';
            return {
                checkUser: function() {
                    var promise = $http.post(apiUrl + 'auth/check/');

                    var thiz = this;

                    promise.then(function(response) {
                        if (response.data.success) {
                            thiz.setUser(response.data.message);
                        }
                    });

                    return promise
                },

                getUser: function() {
                    return currentUser;
                },

                setUser: function(username) {
                    currentUser = username;
                }
            }
        })
})();