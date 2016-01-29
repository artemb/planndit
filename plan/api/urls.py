from django.conf.urls import url, include

from plan.api.views import RouteViewset, order_import, OrderViewset, OrderItemViewset, geocode, VehicleViewset, \
    update_route_vehicle, update_route_orders, resequence, remove_route_order

route_urls = [
    url(r'^$', RouteViewset.as_view({'post': 'list'}), name='route-list'),
    url(r'^create', RouteViewset.as_view({'post': 'create'}), name='route-create'),
    url(r'^(?P<pk>[0-9]+)', RouteViewset.as_view({'post': 'retrieve'}), name='route-detail'),
    url(r'^update_vehicle', update_route_vehicle, name='route-update-vehicle'),
    url(r'^update_orders', update_route_orders, name='route-update-orders'),
    url(r'^remove_order', remove_route_order, name='route-update-orders'),
    url(r'^resequence', resequence, name='route-update-orders'),
]

order_urls = [
    url(r'^item/create', OrderItemViewset.as_view({'post': 'create'}), name='orderitem-create'),
    url(r'^item/(?P<pk>[0-9]+)', OrderItemViewset.as_view({'post': 'update'}), name='orderitem-update'),
    url(r'^(?P<pk>[0-9]+)', OrderViewset.as_view({'get': 'retrieve', 'post': 'update'}), name='order-detail'),
]

vehicle_urls = [
    url(r'^$', VehicleViewset.as_view({'post': 'list'})),
]

urlpatterns = [
    url(r'^route/', include(route_urls)),
    url(r'^order/', include(order_urls)),
    url(r'^vehicle/', include(vehicle_urls)),
    url(r'^import', order_import, name='import'),
    url(r'^geocode', geocode, name='geocode')
]
