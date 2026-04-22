"""
Watchdog file change listener + SSE push.

Monitors state.json, index.db, and other key files in the PROJECT_ROOT/.wordsmith/ directory,
and notifies all connected frontend clients via SSE whenever changes occur.
"""

import asyncio
import json
import time
from pathlib import Path
from typing import AsyncGenerator

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent


class _WebnovelFileHandler(FileSystemEventHandler):
    """Monitor only modification/creation events of key files in the .wordsmith/ directory."""

    WATCH_NAMES = {"state.json", "index.db", "workflow_state.json"}

    def __init__(self, notify_callback):
        super().__init__()
        self._notify = notify_callback

    def on_modified(self, event):
        if event.is_directory:
            return
        if Path(event.src_path).name in self.WATCH_NAMES:
            self._notify(event.src_path, "modified")

    def on_created(self, event):
        if event.is_directory:
            return
        if Path(event.src_path).name in self.WATCH_NAMES:
            self._notify(event.src_path, "created")


class FileWatcher:
    """Manages watchdog Observer and SSE client subscriptions."""

    def __init__(self):
        self._observer: Observer | None = None
        self._subscribers: list[asyncio.Queue] = []
        self._loop: asyncio.AbstractEventLoop | None = None

    # --- Subscription Management ---

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=64)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        try:
            self._subscribers.remove(q)
        except ValueError:
            pass

    # --- Push ---

    def _on_change(self, path: str, kind: str):
        """Called in watchdog thread, dispatches notifications to the main event loop."""
        msg = json.dumps({"file": Path(path).name, "kind": kind, "ts": time.time()})
        if self._loop and not self._loop.is_closed():
            self._loop.call_soon_threadsafe(self._dispatch, msg)

    def _dispatch(self, msg: str):
        dead: list[asyncio.Queue] = []
        for q in self._subscribers:
            try:
                q.put_nowait(msg)
            except asyncio.QueueFull:
                dead.append(q)
        for dq in dead:
            self.unsubscribe(dq)

    # --- Lifecycle ---

    def start(self, watch_dir: Path, loop: asyncio.AbstractEventLoop):
        """Start watchdog observer, listening on watch_dir."""
        self._loop = loop
        handler = _WebnovelFileHandler(self._on_change)
        self._observer = Observer()
        self._observer.schedule(handler, str(watch_dir), recursive=False)
        self._observer.daemon = True
        self._observer.start()

    def stop(self):
        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=3)
            self._observer = None
