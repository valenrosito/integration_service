
# Overview

**Última edición:** 2025-09-20T03:10:29Z

Servicio de integración **MSSQL → API** que sincroniza **Turnos** y **Órdenes** con incrementalidad y ventana de seguridad, asegurando **idempotencia** y **retries**. Despliegue en VM del concesionario vía **Task Scheduler** o **NSSM**.

## Alcance
- Tablas: `dbo.serviciosturnos`, `dbo.serviciosordenes`, `dbo.clientes`, `dbo.unidades`.
- Incrementalidad: `FechaUltimaActualizacion` para turnos; `Apertura` para órdenes.
- Ventana de seguridad: re-lectura de últimos **10 min** por corrida.
- Frecuencia sugerida: cada **10 min**.

## KPIs
- Latencia origen→API (promedio horario hábil).
- Tasa de error HTTP.
- Duplicados (idempotencia).
- Cobertura de campos críticos.
