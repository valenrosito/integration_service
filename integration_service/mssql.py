import pyodbc
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .config import SETTINGS

class MSSQLConnector:
    def __init__(self):
        self.conn = self._connect()

    def _connect(self):
        conn_str = (
            f'DRIVER={{{SETTINGS.mssql_odbc_driver}}};'
            f'SERVER={SETTINGS.mssql_server};'
            f'DATABASE={SETTINGS.mssql_database};'
            f'UID={SETTINGS.mssql_username};'
            f'PWD={SETTINGS.mssql_password};'
            f'TrustServerCertificate={SETTINGS.mssql_trust_server_certificate};'
            'Encrypt=yes;'
        )
        return pyodbc.connect(conn_str, autocommit=False)

    def fetch_turnos(self, since: datetime, window_min: int) -> List[Dict[str, Any]]:
        since_adj = since - timedelta(minutes=window_min) if since else datetime.utcnow() - timedelta(minutes=window_min)
        sql = """
        SELECT IdTurnos, Fecha, Hora, Observaciones, Cliente, Patente, FechaUltimaActualizacion
        FROM dbo.serviciosturnos WITH (NOLOCK)
        WHERE FechaUltimaActualizacion >= ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, since_adj)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def fetch_ordenes(self, since: datetime, window_min: int) -> List[Dict[str, Any]]:
        since_adj = since - timedelta(minutes=window_min) if since else datetime.utcnow() - timedelta(minutes=window_min)
        sql = """
        SELECT OrdenId, NumeroOrden, Observaciones, Apertura, FechaEntrega, CodigoCliente, Automotor, Kms
        FROM dbo.serviciosordenes WITH (NOLOCK)
        WHERE Apertura >= ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, since_adj)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def fetch_cliente(self, codigo: str) -> Dict[str, Any]:
        sql = "SELECT Codigo, Nombre, Telefono, Celular FROM dbo.clientes WITH (NOLOCK) WHERE Codigo = ?"
        cur = self.conn.cursor()
        cur.execute(sql, codigo)
        row = cur.fetchone()
        return dict(zip([d[0] for d in cur.description], row)) if row else {}

    def fetch_unidad(self, patente: str = None, vin: str = None) -> Dict[str, Any]:
        cur = self.conn.cursor()
        if patente:
            cur.execute("SELECT UnidadID, Marca, Modelo, Patente, VIN, AnioProduccion, Kilometros, Version FROM dbo.unidades WHERE Patente = ?", patente)
            row = cur.fetchone()
            if row: return dict(zip([d[0] for d in cur.description], row))
        if vin:
            cur.execute("SELECT UnidadID, Marca, Modelo, Patente, VIN, AnioProduccion, Kilometros, Version FROM dbo.unidades WHERE VIN = ?", vin)
            row = cur.fetchone()
            if row: return dict(zip([d[0] for d in cur.description], row))
        return {}
