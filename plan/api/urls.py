from django.conf.urls import url, include

from plan.api.views import update_route_vehicle, update_route_orders, remove_route_order, resequence, send, order_import, \
    geocode, auth_login, check_login, auth_logout
from plan.api.viewsets import RouteViewset, OrderViewset, OrderItemViewset, VehicleViewset

route_urls = [
    url(r'^$', RouteViewset.as_view({'post': 'list'}), name='route-list'),
    url(r'^create', RouteViewset.as_view({'post': 'create'}), name='route-create'),
    url(r'^(?P<pk>[0-9]+)', RouteViewset.as_view({'post': 'retrieve'}), name='route-detail'),
    url(r'^update_vehicle', update_route_vehicle, name='route-update-vehicle'),
    url(r'^update_orders', update_route_orders, name='route-update-orders'),
    url(r'^remove_order', remove_route_order, name='route-update-orders'),
    url(r'^resequence', resequence, name='route-update-orders'),
    url(r'^send', send, name='route-send'),
]

order_urls = [
    url(r'^item/create', OrderItemViewset.as_view({'post': 'create'}), name='orderitem-create'),
    url(r'^item/(?P<pk>[0-9]+)', OrderItemViewset.as_view({'post': 'update'}), name='orderitem-update'),
    url(r'^(?P<pk>[0-9]+)', OrderViewset.as_view({'get': 'retrieve', 'post': 'update'}), name='order-detail'),
]

vehicle_urls = [
    url(r'^$', VehicleViewset.as_view({'post': 'list'})),
]

auth_urls = [
    url(r'check', check_login, name='auth-check'),
    url(r'login', auth_login, name='auth-login'),
    url(r'logout', auth_logout, name='auth-logout'),
]

urlpatterns = [
    url(r'^auth/', include(auth_urls)),
    url(r'^route/', include(route_urls)),
    url(r'^order/', include(order_urls)),
    url(r'^vehicle/', include(vehicle_urls)),
    url(r'^import', order_import, name='import'),
    url(r'^geocode', geocode, name='geocode'),

]
