from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from plan.api.serializers import RouteSerializer, OrderSerializer, OrderItemSerializer, LocationSerializer, \
    VehicleSerializer
from plan.externals import gis, scheduler
from plan.models import Route, Order, OrderItem, Vehicle


class RouteViewset(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    filter_fields = ('date',)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class VehicleViewset(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


@api_view(['POST'])
def geocode(request):
    address = request.data.get('address')
    location = gis.get_location(address=address)
    response = LocationSerializer(location)
    return Response(response.data)


# [{"ref":"name", "additionals": [{"key": "title", "value": "tip"}]}]
@api_view(['POST'])
@parser_classes((JSONParser,))
def order_import(request):
    def process_order(order, route_id, number):
        address = order.get('address')
        if address is None:
            return False
        location = gis.get_location(address)
        if location is None:
            return False
        comments = order.get('comments', '')
        reference = order.get('reference', '')
        order_model = Order.objects.create(location=location, reference=reference, commentary=comments,
                                           route_id=route_id, order=number)
        for item in order.get('additional', []):
            key = item.get('key')
            value = item.get('value')
            if key is None or value is None:
                continue
            OrderItem.objects.create(order=order_model, key=key, value=value)
        return location.is_valid

    route_id = request.data.get('routeId')
    orders = request.data.get('orders')

    current_orders = Order.objects.filter(route_id=route_id, location__is_valid=True).order_by('order')
    number = current_orders.count() - 1
    last_order = current_orders.last()

    for row in orders:
        if process_order(row, route_id, number):
            number += 1

    last_order.order = number
    last_order.save()

    return Response(request.data)


@api_view(['POST'])
def update_route_vehicle(request):
    route_id = request.data.get('routeId')
    vehicle_id = request.data.get('vehicleId')
    vehicle = Vehicle.objects.filter(account=request.user.account, id=vehicle_id)  # todo make until date check
    if vehicle.count() != 1:
        return Response({'success': False, 'message': 'Vehicle not found'})
    route = Route.objects.filter(account=request.user.account, id=route_id)
    if route.count() != 1:
        return Response({'success': False, 'message': 'Route not found'})
    route = route[0]
    route.vehicle_id = vehicle[0].id
    route.save()
    return Response({'success': True})


@api_view(['POST'])
def update_route_orders(request):
    route_id = request.data.get('routeId')
    orders = request.data.get('orders')
    route = Route.objects.filter(account=request.user.account, id=route_id)
    if route.count() != 1:
        return Response({'success': False, 'message': 'Route not found'})
    route_orders = Order.objects.filter(route__account=request.user.account, route_id=route_id, location__is_valid=True)
    for route_order in route_orders:  # check orders
        order_number = orders.get(str(route_order.id), None)
        if order_number is None:
            return Response({'success': True, 'message': 'Missing order in request: {id}'.format(id=route_order.id)})
    for route_order in route_orders:
        order_number = orders.get(str(route_order.id))
        route_order.order = order_number
        route_order.save()

    return Response({'success': True})  # todo send distances


@api_view(['POST'])
def remove_route_order(request):
    route_id = request.data.get('routeId')
    order_id = request.data.get('orderId')
    route = Route.objects.filter(account=request.user.account, id=route_id)
    if route.count() != 1:
        return Response({'success': False, 'message': 'Route not found'})
    route = route[0]
    order = route.orders.filter(id=order_id)
    if order.count() == 0:
        return Response({'success': False, 'message': 'Order not found'})
    order = order[0]
    if order.location.is_valid:
        deleted = order.delete()
        if deleted:
            route_orders = route.orders.filter(location__is_valid=True)
            for number, route_order in enumerate(route_orders):
                route_order.order = number
                route_order.save()
        else:
            return Response({'success': False, 'message': 'Order cant be deleted'})
    else:
        deleted = order.delete()
        if not deleted:
            return Response({'success': False, 'message': 'Order cant be deleted'})
    return Response({'success': True})


@api_view(['POST'])
def resequence(request):
    route_id = request.data.get('routeId')
    route = scheduler.resequence(route_id, request.user.account.id)
    result = RouteSerializer(route)
    return Response(result.data)
