import logging
from io import StringIO
import requests
import csv
from plan.models import Vehicle, Route

logger = logging.getLogger('planndit.externals.vehicles')
webfleet_url = 'https://csv.business.tomtom.com/extern'


def vehicle_sync(user):
    if user.account.webfleet_account == '':
        return
    reader = webfleet_request(user, 'showObjectReportExtern')

    account_id = user.account.id
    vehicles = Vehicle.objects.filter(account_id=account_id)
    vehicles_map = {}
    for vehicle in vehicles:
        vehicles_map[vehicle.external_id] = vehicle

    new_vehicle = []
    update_vehicles = []

    def diff_vehicle(vehicle, data):
        return vehicle.external_id != data['objectno'] or vehicle.name != data['objectname']

    for row in reader:
        try:
            vehicle = vehicles_map[row['objectno']]
            if vehicle is not None:
                if diff_vehicle(vehicle, row):
                    update_vehicles += [[vehicle, row]]
                vehicles_map.pop(row['objectno'])
        except KeyError as e:
            new_vehicle += [row]
            pass

    object_update = 0

    for vehicleData in new_vehicle:
        vehicle = Vehicle(account=user.account)
        vehicle = update_vehicle(vehicle=vehicle, data=vehicleData)
        vehicle.save()
        object_update += 1

    for vehicleData in update_vehicles:
        vehicle = vehicleData[0]
        vehicle = update_vehicle(vehicle=vehicle, data=vehicleData[1])
        vehicle.save()
        object_update += 1

    # for vehicleData in vehicles_map:
    #    todo to be deleted

    return object_update


def send_orders(account, route_id):
    route = Route.objects.filter(account=account, id=route_id)
    if route.count() != 1:
        return
    route = route[0]

    orders = route.orders.filter(location__is_valid=True).all()
    for number, order in enumerate(orders):
        description = "#{number} {description}".format(number=number, description=order.commentary)
        for item in order.orderitem_set.all():
            description += "\n{key}: {value}".format(key=item.key, value=item.value)
        data = {
            'objectno': route.vehicle.external_id,
            'orderid': order.id,
            'ordertext': description,
            'ordertype': 3,
            'longitude': round(order.location.longitude * 1000000),
            'latitude': round(order.location.latitude * 1000000),
            'city': order.location.city,
            'zip': order.location.postcode,
            'orderdate': route.date.strftime("%d/%m/%y") + "'TZ",  # todo format
        }
        webfleet_request(account, 'sendDestinationOrderExtern', data)
    route.status = 'SEND'
    route.save()


def webfleet_request(account, action, params=None):
    if not params:
        params = {}
    params.update(get_auth(account))
    params['lang'] = 'en'
    params['action'] = action
    result = requests.get(webfleet_url, params)
    reader = parse_csv(result.text)
    return reader  # for row in reader: row['col_name']


def parse_csv(response):
    f = StringIO(response)
    reader = csv.DictReader(f, delimiter=';')
    return reader


def get_auth(account):
    return {
        'account': account.webfleet_account,
        'username': account.webfleet_username,
        'password': account.webfleet_password,
    }


def update_vehicle(vehicle, data):
    vehicle.name = data['objectname']
    vehicle.external_id = data['objectno']
    return vehicle
