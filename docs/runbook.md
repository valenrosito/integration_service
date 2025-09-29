
# Runbook

## Arranque manual
```bash
python -m integration_service.main --dry-run
python -m integration_service.main
```

## Programación
- Task Scheduler: `scripts/create_task_scheduler.ps1`

## Rollback
1. Parar tarea/servicio.
2. Restaurar último `backups/state-*.json` sobre `state.json`.
3. Reanudar tarea/servicio.

## Logs
- Carpeta `logs/` con rotación 10 MB.
