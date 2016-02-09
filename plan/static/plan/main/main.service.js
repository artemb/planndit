/**
 * Created by Sekai Kagami on 02.02.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .factory('mainService', function() {
            var order;

            return {
                getOrder: function() {
                    return order;
                }
            }
        })
})();