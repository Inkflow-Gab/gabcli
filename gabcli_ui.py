"""Terminal presentation helpers for GabCli.

This module intentionally uses only the Python standard library so a release can
run on a clean Python installation without a dependency download.
"""

from __future__ import annotations

import itertools
import os
import sys
import threading
from typing import Any, Optional


RESET = "\033[0m"
SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")


def paint(text: str, code: str, plain: bool = False) -> str:
    """Color text unless plain output was requested."""
    return text if plain else f"\033[{code}m{text}{RESET}"


def supports_color(stream: Any = None) -> bool:
    stream = stream or sys.stdout
    return bool(getattr(stream, "isatty", lambda: False)()) and not bool(os.environ.get("NO_COLOR"))


class Activity:
    """Animated, thread-safe status line used while waiting for the API.

    The animation is stopped before model text or tool output is printed, so it
    never overwrites the answer. Hidden reasoning is represented as a short
    status label only; private chain-of-thought is not displayed.
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled and sys.stderr.isatty()
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._phase = "thinking"
        self._detail = ""
        self._usage: Any = None

    def show(self, phase: str, detail: str = "", usage: Any = None) -> None:
        if not self.enabled:
            return
        with self._lock:
            self._phase = phase
            self._detail = detail
            self._usage = usage
        if self._thread is None or not self._thread.is_alive():
            self._stop.clear()
            self._thread = threading.Thread(target=self._animate, name="gabcli-spinner", daemon=True)
            self._thread.start()

    def _animate(self) -> None:
        for frame in itertools.cycle(SPINNER_FRAMES):
            if self._stop.is_set():
                return
            with self._lock:
                phase = self._phase
                detail = self._detail
                usage = self._usage
            line = f"{frame} {phase}"
            if detail:
                line += f" — {detail}"
            if usage is not None:
                line += f"    {usage.line()}"
            try:
                sys.stderr.write("\r\033[2K" + line)
                sys.stderr.flush()
            except (OSError, ValueError):
                return
            if self._stop.wait(0.12):
                return

    def clear(self) -> None:
        if not self.enabled:
            return
        self._stop.set()
        thread = self._thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=0.35)
        self._thread = None
        try:
            sys.stderr.write("\r\033[2K")
            sys.stderr.flush()
        except (OSError, ValueError):
            pass
