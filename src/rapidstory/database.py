import os
import sqlite3
import threading
import time
from typing import List, Optional, Set
from functools import lru_cache


class DatabaseRepository:
    """Gère l'accès à la base de données SQLite (sync)."""

    def __init__(self, db_path: str):
        self.db_path = os.path.expanduser(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Crée les tables et index FTS5 si nécessaire."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL UNIQUE,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS history_fts USING fts5(
                    command, content='history', content_rowid='id'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_command_lower 
                ON history (LOWER(command))
            """)
            conn.commit()

    def insert_command(self, command: str) -> bool:
        """Insère une commande (ignore si existe)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO history (command) VALUES (?)", (command,)
                )
                if cursor.rowcount > 0:
                    cursor.execute(
                        "INSERT INTO history_fts (id, command) VALUES (last_insert_rowid(), ?)",
                        (command,),
                    )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def insert_commands_batch(self, commands: Set[str]) -> int:
        """Insère plusieurs commandes dédupliquées en batch."""
        inserted = 0
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                conn.execute("BEGIN")
                for cmd in commands:
                    cursor.execute(
                        "INSERT OR IGNORE INTO history (command) VALUES (?)", (cmd,)
                    )
                    if cursor.rowcount > 0:
                        inserted += 1
                        cursor.execute(
                            "INSERT INTO history_fts (id, command) VALUES (last_insert_rowid(), ?)",
                            (cmd,),
                        )
                conn.commit()
        except sqlite3.Error:
            pass
        return inserted

    def search_commands(self, query: str, limit: int) -> List[str]:
        """Recherche full-text via FTS5 (O(log n))."""
        if not query:
            return []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT command FROM history_fts WHERE history_fts MATCH ? LIMIT ?",
                    (f"{query}*", limit),
                )
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error:
            return []


class HistoryCache:
    """Cache LRU en mémoire pour accès rapide (lazy)."""

    def __init__(self, history_path: str, load_limit: int):
        self.history_path = os.path.expanduser(history_path)
        self.load_limit = load_limit
        self._commands: Optional[List[str]] = None

    @property
    def commands(self) -> List[str]:
        """Getter lazy : charge si besoin via méthode cached."""
        return self._get_commands()

    @lru_cache(maxsize=1)
    def _get_commands(self) -> List[str]:
        """Méthode interne cached pour load lazy."""
        if self._commands is None:
            self._load()
        assert self._commands is not None, "Cache load failed"
        return self._commands.copy()

    def _load(self) -> None:
        """Charge lazy depuis fichier (garde dernière occurrence)."""
        if not os.path.exists(self.history_path):
            self._commands = []
            return
        try:
            with open(self.history_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                recent_lines = lines[-self.load_limit :]
                cleaned = [line.strip() for line in recent_lines if line.strip()]
                # Inverse AVANT déduplication pour garder la dernière occurrence
                self._commands = list(dict.fromkeys(reversed(cleaned)))
        except IOError:
            self._commands = []

    def add_command(self, command: str) -> None:
        """Ajoute au cache (invalide LRU)."""
        self.commands  # Force load
        if self._commands is not None and command not in self._commands:
            self._commands.insert(0, command)
            self._commands = self._commands[: self.load_limit]
        self._get_commands.cache_clear()

    def invalidate(self) -> None:
        """Force reload sur changement."""
        self._commands = None
        self._get_commands.cache_clear()


class HistoryMonitor:
    """Surveille les changements en thread (non-bloquant)."""

    def __init__(self, history_path: str, interval: int, callback):
        self.history_path = os.path.expanduser(history_path)
        self.interval = interval
        self.callback = callback
        self.last_mtime = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Démarre la surveillance en thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Arrête la surveillance."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    def _monitor_loop(self) -> None:
        """Boucle de surveillance en thread."""
        while self._running:
            if os.path.exists(self.history_path):
                try:
                    current_mtime = os.path.getmtime(self.history_path)
                    if current_mtime > self.last_mtime:
                        self.last_mtime = current_mtime
                        self.callback()
                except OSError:
                    pass
            time.sleep(self.interval)


class HistoryManager:
    """
    Gestionnaire principal (threaded monitor, SQL-first pour perf).
    """

    def __init__(
        self, db_path: str, history_path: str, load_limit: int, monitor_interval: int
    ):
        self.db = DatabaseRepository(db_path)
        self.cache = HistoryCache(history_path, load_limit)
        self.monitor = HistoryMonitor(
            history_path, monitor_interval, self._on_history_changed
        )
        self.monitor.start()

    def load_from_file(self) -> None:
        """Charge depuis fichier vers DB/cache, avec dédup."""
        self.cache.invalidate()
        commands_set: Set[str] = set(self.cache.commands)  # Dédupe early
        self.db.insert_commands_batch(commands_set)

    def get_commands(
        self, use_sql: bool = True, query: Optional[str] = None, limit: int = 1000
    ) -> List[str]:
        """Retourne commandes : SQL si query, sinon cache LRU."""
        if query and use_sql:
            return self.db.search_commands(query, limit)
        return self.cache.commands[:limit]

    def _on_history_changed(self) -> None:
        """Callback sur changement."""
        self.load_from_file()
