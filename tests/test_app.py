"""Tests for the QuickeeParts Flask application."""
import os
import tempfile


def test_index(client):
    """Test that the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'QuickeeParts' in response.data
    assert b'Add Junk' in response.data
    assert b'View All Junk' in response.data


def test_add_get(client):
    """Test that the add page loads successfully (GET)."""
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add Junk Item' in response.data
    assert b'name' in response.data
    assert b'description' in response.data
    assert b'category' in response.data


def test_add_post(client):
    """Test that adding a junk item works (POST)."""
    response = client.post('/add', data={
        'name': 'Test Part',
        'description': 'A test part',
        'category': 'engine'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Part' in response.data


def test_list(client):
    """Test that the list page shows items."""
    # First add an item
    client.post('/add', data={
        'name': 'Test Part',
        'description': 'A test part',
        'category': 'engine'
    })
    response = client.get('/list')
    assert response.status_code == 200
    assert b'Test Part' in response.data


def test_list_empty(client):
    """Test that the list page shows a message when empty."""
    response = client.get('/list')
    assert response.status_code == 200
    assert b'No junk items yet' in response.data
