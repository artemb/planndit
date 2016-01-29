/**
 * Created by Sekai Kagami on 20.12.2015.
 */
(function() {

    'use strict';

    angular.module('Planndit', ['ui.router', 'ui.bootstrap', 'leaflet-directive', 'ui.sortable'])
        .config(//['$httpProvider', '$routeProvider',
            function($httpProvider, $stateProvider, $urlRouterProvider, $locationProvider) {

                //Необходимо для работы с Django
                $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
                $httpProvider.defaults.headers.post['Content-Type'] = 'application/json';
                //$httpProvider.defaults.headers.post['Content-Type'] = 'application/json';


                $stateProvider.state('logout', {
                    url: '/logout',
                    onEnter: function($state) {

                    }
                }).state('login', {
                    url: '/login',
                    onEnter: function() {
                        $state.reload();
                    }
                }).state('routeList', {
                    url: '/routes/',
                    templateUrl: templatePath + 'routes.html'
                }).state('route', {
                    url: '/route/:id',
                    templateUrl: templatePath + 'route.html'
                }).state('addAddresses', {
                    url: '/route/:id/addresses',
                    templateUrl: templatePath + 'address.html'
                }).state('addAddresses.table', {
                    templateUrl: templatePath + 'address_table.html'
                }).state('orderEdit', {
                    url: '/route/:routeId/order/:orderId',
                    templateUrl: templatePath + 'order_edit.html'
                }).state("otherwise", {
                    url: "*path",
                    templateUrl: templatePath + '404.html'
                });
                $locationProvider.html5Mode({
                    enabled: true,
                    requireBase: false
                });
            });
}());
