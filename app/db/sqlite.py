import sqlite3
from pathlib import Path

from .base import StorageInterface
from ..schemas.orders import StoredOrder


class SQLiteStorage(StorageInterface):
    def __init__(self, database_path: str | Path) -> None:
        self._database_path = Path(database_path)
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def add_order(self, order: StoredOrder) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO orders (
                    id,
                    address,
                    city,
                    st,
                    description,
                    latitude,
                    longitude,
                    optimized
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                order.to_row(),
            )

    def list_orders(self) -> list[StoredOrder]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    address,
                    city,
                    st,
                    description,
                    latitude,
                    longitude,
                    optimized
                FROM orders
                ORDER BY rowid ASC
                """
            ).fetchall()
        return [self._row_to_order(row) for row in rows]

    def list_unoptimized_orders(self) -> list[StoredOrder]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    address,
                    city,
                    st,
                    description,
                    latitude,
                    longitude,
                    optimized
                FROM orders
                WHERE optimized = 0
                ORDER BY rowid ASC
                """
            ).fetchall()
        return [self._row_to_order(row) for row in rows]

    def mark_orders_optimized(self, order_ids: list[str]) -> None:
        if not order_ids:
            return

        placeholders = ", ".join("?" for _ in order_ids)
        with self._connect() as connection:
            connection.execute(
                f"UPDATE orders SET optimized = 1 WHERE id IN ({placeholders})",
                order_ids,
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._database_path)

    def _initialize_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    st TEXT NOT NULL,
                    description TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    optimized INTEGER NOT NULL
                )
                """
            )

    @staticmethod
    def _row_to_order(row: tuple[str, str, str, str, str, float, float, int]) -> StoredOrder:
        return StoredOrder(
            id=row[0],
            address=row[1],
            city=row[2],
            st=row[3],
            description=row[4],
            latitude=row[5],
            longitude=row[6],
            optimized=bool(row[7]),
        )
