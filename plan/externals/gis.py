from plan.models import Location
import requests
import json

geocode = 'http://nominatim.openstreetmap.org/search'


def get_location(address):
    location = Location.objects.filter(address=address)
    if location.count() == 0:
        geocoded = json.loads(request_location(address))
        if len(geocoded) > 0:
            geocoded = geocoded[0]  # todo По циклу искать наиболее подходящий варианты и предлагать пользователю выбор
            latitude = geocoded.get('lat')
            longitude = geocoded.get('lon')
            loc = geocoded.get('address')
            postcode = loc.get('postcode')
            city = loc.get('town', loc.get('city', loc.get('county', 'uk')))
            location = Location.objects.create(address=address, latitude=latitude, longitude=longitude)
        else:
            location = Location.objects.create(address=address, is_valid=False)
    else:
        location = location[0]
    return location


def request_location(address):
    params = {
        'q': address,
        'accept-language': 'en',
        'limit': '1',
        'format': 'json',
        'countrycodes': 'gb',
        'addressdetails': '1'}

    result = requests.get(geocode, params)
    return result.text
