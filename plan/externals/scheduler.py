import requests
import json

from plan.models import Route

scheduler_url = 'http://scheduler.maxoptra.com/rest/scheduler-api/v1/resequence'
scheduler_account = "6cd47e6fc4704f3685031cc82fd05d20"


def resequence(route_id, account_id):
    route = Route.objects.filter(account_id=account_id, id=route_id)
    if route.count() == 0:
        return
    route = route[0]

    data = {
        'account': {
            'accountId': scheduler_account
        },
        'orders': [

        ]}
    orders = route.orders.filter(location__is_valid=True)
    for order in orders:
        if order.order == 0:
            data['start'] = {
                'latitude': order.location.latitude,
                'longitude': order.location.longitude,
            }
        elif order.order == orders.count() - 1:
            data['end'] = {
                'latitude': order.location.latitude,
                'longitude': order.location.longitude,
            }
        else:
            data['orders'].append({
                'uid': order.id,
                'location': {
                    'latitude': order.location.latitude,
                    'longitude': order.location.longitude,
                }
            })
    params = {
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    response = requests.post(scheduler_url, json=data, **params)
    geocoded = json.loads(response.text)
    if geocoded['success']:
        if geocoded['valid']:
            for order in orders:
                for number, geo_order in enumerate(geocoded['orders']):
                    if order.id == int(geo_order.get('uid')):
                        order.order = number + 1
                        order.save()
                        break
    return route
