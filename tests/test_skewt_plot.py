from src.data_processing import load_json_data
import pytest

def test_load_json_data():
    data = load_json_data('data/windy_sounding3.json')
    assert data is not None
    assert 'features' in data
