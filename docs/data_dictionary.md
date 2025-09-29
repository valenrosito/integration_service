
# Data Dictionary

## Fuentes
- **Turnos (T)**: dbo.serviciosturnos
- **Órdenes (O)**: dbo.serviciosordenes
- **Clientes (C)**: dbo.clientes
- **Unidades (U)**: dbo.unidades

## Mapeo API ← Legacy (resumen)
- `appointment_date`: T.Fecha + T.Hora | O.Apertura (fallback O.FechaEntrega)
- `appointment_status`: T→scheduled | O→confirmed
- `vehicle_id`: T.Patente (fallback U.VIN) | O.Automotor→U.Patente (fallback VIN)
- `customer_name/phone`: T.ClienteNombre | C.Nombre; C.Telefono/C.Celular
