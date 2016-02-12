/**
 * Created by Sekai Kagami on 12.02.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('LoginController',[
            '$scope', 'authService', 'mainService', '$state',
            function($scope, authService, mainService, $state) {
                $scope.username = '';
                $scope.password = '';

                $scope.login = function() {
                    authService.login($scope.username, $scope.password).then(function(response) {
                        console.log(response.data);
                        if (!response.data.success) {
                            $scope.error = response.data.message;
                        } else {
                            mainService.setUser(response.data.message);
                            $scope.$emit('userUpdate');
                            $state.go('routeList');
                        }
                    })
                }
            }])
})();