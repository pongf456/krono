import asyncio
from src.bot.domain.types import Database, Client
import sqlite3


class DatabaseSqlite(Database):
    DB_NAME = "clients.db"

    def __init__(self) -> None:
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    identifier INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """
            )
            conn.commit()

    async def _execute_command(
        self, sql_command: str, params: tuple = ()
    ) -> list[sqlite3.Row]:
        loop = asyncio.get_running_loop()

        def run_sync():
            with sqlite3.connect(self.DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(sql_command, params)
                conn.commit()
                return cursor.fetchall()

        return await loop.run_in_executor(None, run_sync)

    async def store(self, client: Client) -> None:
        sql = "INSERT OR REPLACE INTO clients (identifier, name) VALUES (?, ?)"
        await self._execute_command(sql, (client["identifier"], client["name"]))

    async def get(self, identifier: int) -> Client | None:
        sql = "SELECT identifier, name FROM clients WHERE identifier = ?"
        results = await self._execute_command(sql, (identifier,))

        if not results:
            return None

        row = results[0]
        return Client(identifier=row["identifier"], name=row["name"])

    async def all(self) -> list[Client]:
        sql = "SELECT identifier, name FROM clients"
        results = await self._execute_command(sql)

        return [
            Client(identifier=row["identifier"], name=row["name"]) for row in results
        ]

    async def delete(self, identifier: int) -> Client | None:
        client_to_delete = await self.get(identifier)

        if client_to_delete:
            sql = "DELETE FROM clients WHERE identifier = ?"
            await self._execute_command(sql, (identifier,))

        return client_to_delete
