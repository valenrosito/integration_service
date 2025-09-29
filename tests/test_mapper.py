
from integration_service.mapper import is_payload_acceptable

def test_accept_minimum_fields():
    p = {
        "appointment_date": "2024-01-01T00:00:00",
        "appointment_status": "scheduled",
        "vehicle_id": "ABC123",
        "customer_name": "Juan"
    }
    assert is_payload_acceptable(p) is True

def test_reject_missing_vehicle():
    p = {
        "appointment_date": "2024-01-01T00:00:00",
        "appointment_status": "scheduled",
        "vehicle_id": None,
        "customer_name": "Juan"
    }
    assert is_payload_acceptable(p) is False
