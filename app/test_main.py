from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK
from main import app
from fastapi import status

client = TestClient(app)

id = 2

data = [
    {
    "country_region": "Singapore",
    "province_state": None,
    "date": "2021-05-05",
    "lat": None,
    "long_": None,
    "confirmed": 1,
    "deaths": 1,
    "recovered": 1,
    "active": 1,
    "incident_rate": 0.1,
    "case_fatality_ratio": 0.2
    },
    {
    "country_region": "Singapore",
    "province_state": None,
    "date": "2021-05-06",
    "lat": None,
    "long_": None,
    "confirmed": 1,
    "deaths": 1,
    "recovered": 1,
    "active": 1,
    "incident_rate": 0.1,
    "case_fatality_ratio": 0.2
    },
    {
    "country_region": "Singapore",
    "province_state": None,
    "date": "2021-05-07",
    "lat": None,
    "long_": None,
    "confirmed": None,
    "deaths": 1,
    "recovered": 1,
    "active": 1,
    "incident_rate": 0.1,
    "case_fatality_ratio": 0.2
    }]


def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "Hello World"}

def test_create_report():
    response = client.post("/reports/", json=data[0])
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post("/reports/", json=data[1])
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post("/reports/", json=data[2])
    assert response.status_code == status.HTTP_201_CREATED

def test_get_report():
    response = client.get(f"/reports/{id}")
    assert response.status_code == status.HTTP_200_OK

def test_update_report():
    data_update = data[1]
    data_update["confirmed"] = 20
    response = client.put(f"/reports/{id}", json=data_update)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_update_bad_report():
    response = client.put(f"/reports/-1", json=data[0])
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_read_bad_world_summary_1():
    response = client.get("/reports/world?filter_date=2124-01-01")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_read_world_summary():
    response = client.get("/reports/world?filter_date=2021-05-05")
    assert response.status_code == status.HTTP_200_OK

def test_read_bad_country_report():
    response = client.get("/reports/?country_region=Singapore&date_from=2021-01-01&date_to=2020-01-01")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_read_country_report():
    response = client.get("/reports/?country_region=Singapore&date_from=2020-01-01&date_to=2021-05-06")
    assert response.status_code == status.HTTP_200_OK

def test_read_bad_country_daily_report_1():
    response = client.get('/daily/?country_region=Singapore&_date=2020-01-01')
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_read_country_daily_report():
    response = client.get('/daily/?country_region=Singapore&_date=2021-05-06')
    assert response.status_code == status.HTTP_200_OK

def test_read_bad_world_daily_report():
    response = client.get("/daily/world?filter_date=2020-01-01")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_read_world_daily_report():
    response = client.get("/daily/world?filter_date=2021-05-06")
    assert response.status_code == status.HTTP_200_OK

def test_delete_report():
    response = client.delete(f"/reports/{id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_bad_report():
    response = client.delete(f"/reports/-1", json=data[0])
    assert response.status_code == status.HTTP_404_NOT_FOUND