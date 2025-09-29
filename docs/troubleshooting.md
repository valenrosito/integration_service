
# Troubleshooting

- **Error ODBC / Login failed**: verificar `.env` (usuario read-only, driver).
- **Timeout a API**: revisar salida 443, firewall, ALLOWED_HOSTS.
- **Muchos duplicados**: confirmar que `Idempotency-Key` es estable y que no se resetea `state.json`.
- **Cobertura <95%**: revisar validaciones y orígenes de `customer_*` y vehículo.
