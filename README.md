
# Integration Service – MSSQL → API

Servicio Python para integrar **turnos** y **órdenes** desde SQL Server hacia una API HTTP con **incrementalidad**, **ventana de seguridad**, **idempotencia**, **retries** y almacena **estado local**.

## Estructura

```
integration_service/
  ├─ config.py
  ├─ logger.py
  ├─ state.py
  ├─ mssql.py
  ├─ mapper.py
  ├─ sender.py
  ├─ main.py
  └─ utils.py
scripts/
  ├─ create_task_scheduler.ps1
  ├─ remove_task_scheduler.ps1
  ├─ install_service_nssm.ps1
  ├─ uninstall_service_nssm.ps1
  └─ run_once.bat
docs/
  ├─ overview.md
  ├─ data_dictionary.md
  ├─ runbook.md
  ├─ troubleshooting.md
  └─ changelog.md
.env.example
requirements.txt
README.md
```

## Quickstart

1. Crear y activar venv, instalar dependencias:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  
   pip install -r requirements.txt
   ```
2. Copiar `.env.example` a `.env` y completar valores.
3. Probar conexión:
   ```bash
   python -m integration_service.main --dry-run
   ```
4. Programar ejecución:
   - **Task Scheduler** cada 10 min: `scripts/create_task_scheduler.ps1`

## Criterios & Operación

- **Latencia objetivo** ≤ 10 min (ventana y frecuencia configurables).
- **Error rate** < 1% y **0 duplicados** usando `Idempotency-Key`.
- **Cobertura de campos críticos** monitoreada en logs.
- **Rollback**: detener tarea/servicio, restaurar `backups/state-*.json`.
