/**
 * Created by Sekai Kagami on 12.01.2016.
 */

(function() {

    'use strict';

    angular.module('Planndit')
        .controller('MapController', [
            '$scope', 'routeService', '$stateParams', '$state',
            function ($scope, routeService, $stateParams, $state) {
				var self = this;
                $scope.center = {
                    lat: 51.5085300,
					lng: -0.1257400,
					zoom: 9
                };
                $scope.markers = {
				};
				$scope.paths = {
					path: {
						color: '#2299FF',
						weight: 2,
						latlngs: []
					}
				};
				$scope.defaults = {
					scrollWheelZoom: false
				};
				self.setRoute = function(route) {
					self.route = route;
					self.showRoute(self.route);
				};

				self.addOrderMarker = function(order, draggable) {
					var marker = {
						lat: parseFloat(order.location.latitude),
						lng: parseFloat(order.location.longitude),
						message: order.address,
						draggable: draggable,
						icon: {
							iconUrl: imagePath + "map-marker-3.png",
							iconSize: [30, 40],
							iconAnchor: [15, 40]
						},
						label: {
							message: order.order + "",
							options: {
								noHide: true,
								offset: [-13, -41],
								className: 'order-number'
							}
						}
					};
					$scope.markers[order.id + '_' + order.order] = marker;
				};

				self.addLocationMarker = function(location, label) {
					var locationKey = 'location_' + location.id;
					if ($scope.markers.hasOwnProperty(locationKey)) {
						return
					}
					var marker = {
						lat: parseFloat(location.latitude),
						lng: parseFloat(location.longitude),
						draggable: false,
						icon: {
							iconUrl: imagePath + "map-marker-3.png",
							iconSize: [30, 40],
							iconAnchor: [15, 40]
						},
						label: {
							message: label,
							options: {
								noHide: true,
								offset: [-13, -41],
								className: 'order-number'
							}
						}
					};
					$scope.markers[locationKey] = marker;
				};

				self.showRoute = function(route) {
					$scope.markers = {};
					$scope.paths.path.latlngs = [];
					var bounds = new L.LatLngBounds();

					//start
					self.addLocationMarker(route.start_location, 'S');
					var lat = parseFloat(route.start_location.latitude);
					var lng = parseFloat(route.start_location.longitude);
					var path = {
						lat: lat,
						lng: lng
					};
					bounds.extend(L.latLng(lat, lng));
					$scope.paths.path.latlngs.push(path);
					//orders
					for (var i = 0; i < route.orders.length; i++) {
						var order = route.orders[i];
						self.addOrderMarker(order, false);
						lat = parseFloat(order.location.latitude);
						lng = parseFloat(order.location.longitude);
						path = {
							lat: lat,
							lng: lng
						};
						bounds.extend(L.latLng(lat, lng));
						$scope.paths.path.latlngs.push(path);
					}
					//end
					self.addLocationMarker(route.end_location, 'E');
					lat = parseFloat(route.end_location.latitude);
					lng = parseFloat(route.end_location.longitude);
					path = {
						lat: lat,
						lng: lng
					};
					bounds.extend(L.latLng(lat, lng));
					$scope.paths.path.latlngs.push(path);
					$scope.bounds = {
						southWest: bounds.getSouthWest(),
						northEast: bounds.getNorthEast()
					};
				};

				self.showOrder = function(order) {
					$scope.markers = {};
					$scope.paths.path.latlngs = [];
					if (order.location.is_valid) {
					    var bounds = new L.LatLngBounds();
						self.addOrderMarker(order, true)
                        var lat = parseFloat(order.location.latitude);
						var lng = parseFloat(order.location.longitude);
						bounds.extend(L.latLng(lat, lng));
                        $scope.bounds = {
                            southWest: bounds.getSouthWest(),
                            northEast: bounds.getNorthEast()
                        };
					}
				};
				$scope.$on('routeUpdate', function(event, data) {
					self.setRoute(routeService.getCurrentRoute());
				});
				$scope.$on('showOrder', function(event, data) {
					self.showOrder(data);
				})
            }])
})();