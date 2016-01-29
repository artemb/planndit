/**
 * Created by Sekai Kagami on 25.12.2015.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('AddressController',[
            '$scope', 'addressService', '$stateParams', '$state',
            function($scope, addressService, $stateParams, $state) {
                var self = this;

                self.table = [];
                self.addresses = "name;London;new order;add1;add2";

                self.defaultHeaders = [
                    {id: 'reference', name: 'Reference'},
                    {id: 'address', name: 'Address'},
                    {id: 'comments', name: 'Comments'},
                    {id: 'additional', name: 'Additional info', key: ''}
                ];
                self.headers = [];

                $scope.select = function(index, header) {
                    //delete header.$$hashKey;
                    self.headers[index] = angular.copy(header);
                };

                $scope.import = function() {
                    if (!self.table.length) {
                        var delimiter = ';';
                        var lines = self.addresses.split('\n');
                        for (var i = 0; i < lines.length; i++) {
                            var line = lines[i];
                            var row = line.split(delimiter);
                            if (self.headers.length < row.length) {
                                if (self.headers.length < self.defaultHeaders.length) {
                                    self.headers = angular.copy(self.defaultHeaders.slice(self.headers.length, Math.min(self.defaultHeaders.length, row.length))); //todo Использовать список с сервера
                                }
                                for (var j = 0, l=row.length - self.headers.length; j < l; j++) {
                                    self.headers.push({id: 'additional', name: 'Additional info', key: ''});
                                }
                            }
                            self.table.push(row);
                        }
                        for (i = 0; i < self.table.length; i++) {
                            var row = self.table[i];
                            if (row.length < self.headers.length) {
                                for (j = row.length; j < self.headers.length; j++) {
                                    row.push('');
                                }
                            }
                        }
                        $state.go('addAddresses.table');
                    } else {
                        //send
                        var data = [];
                        for (i = 0; i < self.table.length; i++) {
                            var row = self.table[i];
                            var order = {
                                additional: []
                            };
                            for (j = 0; j < self.headers.length; j++) {
                                if (self.headers[j].id.length) {
                                    if (self.headers[j].id == "additional") {
                                        order.additional.push({
                                            key: self.headers[j].key,
                                            value: row[j]
                                        });
                                    } else {
                                        order[self.headers[j].id] = row[j];
                                    }
                                }
                            }
                            data.push(order);
                        }
                        addressService.import(data, $stateParams.id).then(function() {
                            $state.go('route', {id: $stateParams.id})
                        });
                    }
                }
            }])
})();