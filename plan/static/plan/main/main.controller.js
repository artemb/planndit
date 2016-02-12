/**
 * Created by Sekai Kagami on 02.02.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('MainController',[
            '$scope', 'mainService', 'authService', '$state',
            function($scope, mainService, authService, $state) {
                mainService.checkUser().then(function() {
                    $scope.username = mainService.getUser();
                });

                $scope.logout = function() {
                    authService.logout().then(function() {
                        delete $scope.username;
                        $state.go('login')
                    });
                };

                $scope.$on('userUpdate', function() {
                    $scope.username = mainService.getUser();
                })
            }])
})();