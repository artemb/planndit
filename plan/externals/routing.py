import json

import requests

from plan.models import LocationCache

router = 'https://router.project-osrm.org/{action}'


def calculate_distance(route):
    request_router(route)


def request_router(route):
    orders = route.orders.filter(location__is_valid=True)
    previous = None

    # first
    first_order = orders.first()
    distance, duration = process_location(route.start_location, first_order.location)
    first_order.distance = distance
    first_order.duration = duration
    first_order.save()
    # orders
    for order in orders:
        if previous is None:
            previous = order
            continue
        distance, duration = process_location(previous.location, order.location)
        order.distance = distance
        order.duration = duration
        order.save()
        previous = order

    # last
    last_order = orders.last()
    distance, duration = process_location(last_order.location, route.end_location)
    route.distance = distance
    route.duration = duration
    route.save()


def process_location(location_from, location_to):
    distance = 0
    duration = 0
    if location_from.latitude != location_to.latitude or location_from.longitude == location_to.longitude:
            cache = get_location_cache(location_from, location_to)
            distance = cache.distance
            duration = cache.duration
    return distance, duration


def get_location_cache(location_from, location_to):
    if location_from.is_valid is False or location_to.is_valid is False:
        return None
    cache = LocationCache.objects.filter(from_latitude=location_from.latitude, from_longitude=location_from.longitude,
                                         to_latitude=location_to.latitude, to_longitude=location_to.longitude)
    if cache.count() > 0:
        return cache[0]
    return request_viaroute(location_from, location_to)


def request_viaroute(location_from, location_to):
    params = {
        'headers': {
            'User-Agent': 'Planndit',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    }
    data = {
        'loc': [
            str(location_from.latitude) + ',' + str(location_from.longitude),
            str(location_to.latitude) + ',' + str(location_to.longitude)
        ],
    }
    raw_response = requests.get(router.format(action='viaroute'), data, **params)
    response = json.loads(raw_response.text)
    distance, duration = parse_response(response)
    cache = LocationCache.objects.create(from_latitude=location_from.latitude, from_longitude=location_from.longitude,
                                         to_latitude=location_to.latitude, to_longitude=location_to.longitude,
                                         distance=distance, duration=duration)
    return cache


def parse_response(response):
    summary = response['route_summary']
    distance = summary.get('total_distance', 0)
    duration = summary.get('total_time', 0)
    return distance, duration
