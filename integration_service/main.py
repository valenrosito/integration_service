from datetime import datetime
import argparse, sys
from .logger import configure_logger
from .state import load_state, save_state, backup_state
from .mssql import MSSQLConnector
from .mapper import map_turno_to_payload, map_orden_to_payload, is_payload_acceptable
from .sender import APISender
from .utils import content_hash
from .config import SETTINGS

logger = configure_logger()

class IntegrationService:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.state = load_state()
        self.db = MSSQLConnector()
        self.sender = APISender()

    def run(self):
        sent, skipped_same, invalid = 0, 0, 0

        # --- Turnos ---
        turnos_since = self._parse_dt(self.state.get("turnos_since"))
        turnos = self.db.fetch_turnos(turnos_since, SETTINGS.security_window_min)
        logger.info(f"Turnos encontrados: {len(turnos)}")

        for t in turnos:
            cliente = self.db.fetch_cliente(t.get("Cliente")) if t.get("Cliente") else {}
            unidad = self.db.fetch_unidad(patente=t.get("Patente"))
            payload = map_turno_to_payload(t, cliente, unidad)

            if not is_payload_acceptable(payload):
                invalid += 1; continue

            h = content_hash(payload)
            key = f"turno:{t.get('IdTurnos')}"
            if self.state.setdefault("seen", {}).get(key) == h and not self.dry_run:
                skipped_same += 1; continue

            if self.dry_run:
                logger.info(f"[DRY] Enviaría turno {t.get('IdTurnos')}")
            else:
                code = self.sender.send(payload, idempotency_key=key)
                logger.info(f"POST turno {t.get('IdTurnos')} -> {code}")
                self.state["seen"][key] = h
                sent += 1

        self.state["turnos_since"] = self._iso_now()

        # --- Órdenes ---
        ordenes_since = self._parse_dt(self.state.get("ordenes_since"))
        ordenes = self.db.fetch_ordenes(ordenes_since, SETTINGS.security_window_min)
        logger.info(f"Órdenes encontradas: {len(ordenes)}")

        for o in ordenes:
            cliente = self.db.fetch_cliente(o.get("CodigoCliente")) if o.get("CodigoCliente") else {}
            unidad = self.db.fetch_unidad(patente=o.get("Automotor"))
            payload = map_orden_to_payload(o, cliente, unidad)

            if not is_payload_acceptable(payload):
                invalid += 1; continue

            h = content_hash(payload)
            key = f"orden:{o.get('OrdenId')}"
            if self.state.setdefault("seen", {}).get(key) == h and not self.dry_run:
                skipped_same += 1; continue

            if self.dry_run:
                logger.info(f"[DRY] Enviaría orden {o.get('OrdenId')}")
            else:
                code = self.sender.send(payload, idempotency_key=key)
                logger.info(f"POST orden {o.get('OrdenId')} -> {code}")
                self.state["seen"][key] = h
                sent += 1

        self.state["ordenes_since"] = self._iso_now()

        if not self.dry_run:
            backup_state()
            save_state(self.state)

        logger.info(f"Resumen: sent={sent}, skipped_same={skipped_same}, invalid={invalid}")

    @staticmethod
    def _iso_now():
        return datetime.utcnow().isoformat() + "Z"

    @staticmethod
    def _parse_dt(s: str):
        if not s: return None
        try:
            return datetime.fromisoformat(s.replace("Z",""))
        except Exception:
            return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    service = IntegrationService(dry_run=args.dry_run)
    try:
        service.run()
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
