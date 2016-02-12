from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from plan.api.data import Record
from plan.api.serializers import RouteSerializer, LocationSerializer
from plan.externals import gis, scheduler, routing, webfleet
from plan.models import Route, Order, OrderItem, Vehicle


@api_view(['POST'])
def check_login(request):
    if request.user is None:
        return Response(Record.serialize(False))
    else:
        return Response(Record.serialize(True, request.user.username))


@api_view(['POST'])
def auth_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or len(username) == 0:
        return Response(Record.serialize(False, 'Username is empty'))
    if password is None or len(password) == 0:
        return Response(Record.serialize(False, 'Password is empty'))
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(Record.serialize(True, user.username))
    else:
        return Response(Record.serialize(False, 'Username or password is incorrect'))


@api_view(['POST'])
def auth_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password_repeat = request.data.get('password_repeat')
    if username is None or len(username) == 0:
        return Response(Record.serialize(False, 'Username is empty'))
    if password is None or len(password) == 0:
        return Response(Record.serialize(False, 'Password is empty'))
    if password is None or len(password) == 0:
        return Response(Record.serialize(False, 'Password is empty'))
    # if form.is_valid():
    #     if password == password_repeat:
    #         user = User.objects.create_user(username=username, password=password)
    #         user.account = Account.objects.create(user_id=user.id)
    #         user.save()
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         return HttpResponseRedirect(reverse('plan:index'))
    #
    # error = form.errors.as_text()
    # logger.warning(error)
    # return render(request, self.template_name, {
    #     'error': error,
    #     'login': username,
    #     'password': password,
    # })


@api_view(['POST'])
def auth_logout(request):
    if request.user:
        logout(request)
        return Response(Record.serialize(True))
    return Response(Record.serialize(False, 'User is not logged in'))


@api_view(['POST'])
def geocode(request):
    address = request.data.get('address')
    location = gis.get_location(address=address)
    response = LocationSerializer(location)
    return Response(response.data)


@api_view(['POST'])
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

    route = Route.objects.filter(id=route_id, account=request.user.account)
    if route.count() != 1:
        return Response({'success': False, 'message': 'Route not found'})
    route = route[0]

    current_orders = route.orders.filter(location__is_valid=True).order_by('order')
    number = current_orders.count() - 1
    last_order = current_orders.last()

    for row in orders:
        if process_order(row, route_id, number):
            number += 1

    last_order.order = number
    last_order.save()

    routing.calculate_distance(route)

    return Response()


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
    route = route[0]
    route_orders = route.orders.filter(location__is_valid=True)
    for route_order in route_orders:  # check orders
        order_number = orders.get(str(route_order.id), None)
        if order_number is None:
            return Response({'success': True, 'message': 'Missing order in request: {id}'.format(id=route_order.id)})
    for route_order in route_orders:
        order_number = orders.get(str(route_order.id))
        route_order.order = order_number
        route_order.save()
    routing.calculate_distance(route)  # todo optimize
    return Response({'success': True, 'route': RouteSerializer(route).data})


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
    routing.calculate_distance(route)  # todo optimize
    return Response({'success': True, 'route': RouteSerializer(route).data})


@api_view(['POST'])
def resequence(request):
    route_id = request.data.get('routeId')
    route = scheduler.resequence(route_id, request.user.account.id)
    result = RouteSerializer(route)
    return Response(result.data)


@api_view(['POST'])
def send(request):
    route_id = request.data.get('routeId')
    webfleet.send_orders(request.user.account, route_id)
    return Response()
