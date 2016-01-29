from plan.models import Location
import requests
import json

geocode = 'http://nominatim.openstreetmap.org/search'


def get_location(address):
    location = Location.objects.filter(address=address)
    if location.count() == 0:
        geocoded = json.loads(request_location(address))
        if len(geocoded) > 0:
            geocoded = geocoded[0]
            latitude = geocoded['lat']
            longitude = geocoded['lon']
            location = Location.objects.create(address=address, latitude=latitude, longitude=longitude)
        else:
            location = Location.objects.create(address=address, is_valid=False)
    else:
        location = location[0]
    return location


def request_location(address):
    params = {
        'q': address + ' gb',  # gb == England, увеличивает шанс нахождения адреса в Англии(Номинатим глупый)
        'accept-language': 'en',
        'limit': '1',
        'format': 'json',
        'addressdetails': '1'}

    result = requests.get(geocode, params)
    return result.text
