import requests
import pytest


def check_zip(zip):
    numbers = zip[:5]
    print(numbers)

    if  [s for s in numbers if s not in '0123456789']:
        return False

    return True


def test_check_status():
    result = requests.get('http://ip-api.com/json')
    data = result.json()
    status = data.get('status')

    assert status == 'success', 'Status is wrong!'


def test_check_country_code():
    result = requests.get('http://ip-api.com/json')
    data = result.json()
    country_code = data.get('countryCode')

    assert country_code == 'RU', 'Country code is wrong!'


def test_check_city():
    result = requests.get('http://ip-api.com/json')
    data = result.json()
    city = data.get('city')

    assert city == 'Moscow', 'City is wrong!'


def test_region():
    result = requests.get('http://ip-api.com/json')
    data = result.json()
    region = data.get('region')

    assert region == 'MOW', 'Region is wrong!'


def test_check_zip():
    result = requests.get('http://ip-api.com/json')
    data = result.json()
    zip = data.get('zip')


    assert zip > ''
    assert len(zip) >= 6
    assert check_zip(zip)


if __name__ == "__main__":
    # в PyCharm удобно запускать как обычный скрипт. Без командной строки
    pytest.main()