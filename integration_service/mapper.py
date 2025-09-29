
from datetime import datetime
from typing import Dict, Any

def _dt(date_val, time_val=None):
    if date_val is None: return None
    if time_val is None:
        try:
            return datetime.combine(date_val, datetime.min.time()).isoformat()
        except Exception:
            return None
    try:
        return datetime.combine(date_val, time_val).isoformat()
    except Exception:
        return None

def map_turno_to_payload(t: Dict[str, Any], cliente: Dict[str, Any], unidad: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "shop_id": 1,
        "appointment_date": _dt(t.get("Fecha"), t.get("Hora")),
        "appointment_status": "scheduled",
        "appointment_comments": t.get("Observaciones"),
        "vehicle_event_type": "Mantenimiento",
        "vehicle_event_number": None,
        "vehicle_id": t.get("Patente") or unidad.get("VIN"),
        "vehicle_brand": unidad.get("Marca"),
        "vehicle_model": unidad.get("Modelo"),
        "vehicle_plate": t.get("Patente") or unidad.get("Patente"),
        "vehicle_vin": unidad.get("VIN"),
        "vehicle_year": unidad.get("AnioProduccion"),
        "vehicle_kms": unidad.get("Kilometros"),
        "vehicle_version": unidad.get("Version"),
        "customer_phone": cliente.get("Telefono") or cliente.get("Celular"),
        "customer_phones": [x for x in [cliente.get("Telefono"), cliente.get("Celular")] if x],
        "customer_name": t.get("ClienteNombre") or cliente.get("Nombre"),
        "customer_alias": ""
    }
    return payload

def map_orden_to_payload(o: Dict[str, Any], cliente: Dict[str, Any], unidad: Dict[str, Any]) -> Dict[str, Any]:
    appointment_date = o.get("Apertura") or o.get("FechaEntrega")
    payload = {
        "shop_id": 1,
        "appointment_date": appointment_date.isoformat() if hasattr(appointment_date, "isoformat") else None,
        "appointment_status": "confirmed",
        "appointment_comments": o.get("Observaciones"),
        "vehicle_event_type": "Reparacion",
        "vehicle_event_number": o.get("NumeroOrden"),
        "vehicle_id": (unidad.get("Patente") or unidad.get("VIN")) if unidad else None,
        "vehicle_brand": unidad.get("Marca") if unidad else None,
        "vehicle_model": unidad.get("Modelo") if unidad else None,
        "vehicle_plate": unidad.get("Patente") if unidad else None,
        "vehicle_vin": unidad.get("VIN") if unidad else None,
        "vehicle_year": unidad.get("AnioProduccion") if unidad else None,
        "vehicle_kms": o.get("Kms") or (unidad.get("Kilometros") if unidad else None),
        "vehicle_version": unidad.get("Version") if unidad else None,
        "customer_phone": (cliente.get("Telefono") or cliente.get("Celular")) if cliente else None,
        "customer_phones": ([x for x in [cliente.get("Telefono"), cliente.get("Celular")] if x] if cliente else []),
        "customer_name": (cliente.get("Nombre") if cliente else None),
        "customer_alias": ""
    }
    return payload

def is_payload_acceptable(p: Dict[str, Any]) -> bool:
    # Validaciones mínimas para cobertura de campos críticos
    crit = [
        p.get("appointment_date"),
        p.get("appointment_status"),
        p.get("vehicle_id"),
        (p.get("customer_name") or p.get("customer_phone"))
    ]
    return all(crit)
