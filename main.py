#!/usr/bin/env python3

import time
import psutil
from rich.live import Live
from rich.console import Console

from core.collector.system import collect_system_snapshot
from core.ui.dashboard import build_layout


def main():
    console = Console()

    psutil.cpu_percent(interval=None)
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except Exception:
            pass

    console.clear()

    try:
        with Live(console=console, screen=True, refresh_per_second=4) as live:
            while True:
                start = time.time()
                snap = collect_system_snapshot()
                live.update(build_layout(snap))
                elapsed = time.time() - start
                time.sleep(max(0, 1 - elapsed))

    except KeyboardInterrupt:
        console.clear()
        console.print("\n[bold bright_cyan]System Pulse[/] [grey50]— session ended[/]\n")


if __name__ == "__main__":
    main()