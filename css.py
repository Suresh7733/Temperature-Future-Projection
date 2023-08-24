import requests

def is_in_india(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}'
    response = requests.get(url).json()
    return response.get('address', {}).get('country') == 'India'

