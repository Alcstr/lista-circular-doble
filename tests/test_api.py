import json
import pytest
import sys, os
from flask import Flask
# Ensure the project root is on the import path for the app module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_health_endpoint(client):
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'ok'
    assert isinstance(data['size'], int)

def test_catalog_endpoint(client):
    resp = client.get('/api/catalog')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'items' in data and isinstance(data['items'], list)
    assert 'current' in data and isinstance(data['current'], dict)
    assert data['size'] == len(data['items'])

def test_navigation_wraparound(client):
    # Get initial current id
    first = client.get('/api/current').get_json()
    # Move previous (should wrap to tail)
    prev = client.post('/api/previous').get_json()
    assert prev['id'] != first['id']
    # Move next back to first
    next_item = client.post('/api/next').get_json()
    assert next_item['id'] == first['id']

def test_select_invalid(client):
    resp = client.post('/api/select/invalid-id')
    assert resp.status_code == 404
    data = resp.get_json()
    assert 'error' in data

def test_search_and_category(client):
    # Search for a known title fragment
    resp = client.get('/api/search?q=Starlight')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['results']) >= 1
    # Category filter
    resp = client.get('/api/category/Action')
    assert resp.status_code == 200
    cat_data = resp.get_json()
    assert isinstance(cat_data['items'], list)
