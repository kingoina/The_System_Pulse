"""
core/ui/dashboard.py

Renders a SystemSnapshot into a full-screen Rich terminal dashboard.
All render_* functions are pure — they take data, return Rich renderables.
build_layout() assembles everything into the final Layout.
"""

import platform
from datetime import datetime

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

from core.models import SystemSnapshot, CPUStats, MemoryStats

# ─────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────

THEME = {
    "normal":   "bright_green",
    "moderate": "yellow",
    "high":     "bright_red",
    "critical": "bold bright_red",
    "dim":      "grey50",
    "header":   "bold bright_cyan",
    "label":    "cyan",
    "border":   "grey35",
    "accent":   "bright_cyan",
    "white":    "bright_white",
    "bg":       "on grey7",
}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def usage_color(pct: float) -> str:
    if pct < 50: return THEME["normal"]
    if pct < 75: return THEME["moderate"]
    if pct < 90: return THEME["high"]
    return THEME["critical"]


def render_bar(pct: float, width: int = 28) -> Text:
    """Render a colored progress bar as a Rich Text object."""
    pct = max(0.0, min(100.0, pct))
    filled = int(round(pct / 100 * width))
    empty  = width - filled
    bar = Text()
    bar.append("█" * filled, style=usage_color(pct))
    bar.append("░" * empty,  style=THEME["dim"])
    return bar


def fmt_bytes(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"


def fmt_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d  %H:%M:%S")


# ─────────────────────────────────────────────
#  PANEL: HEADER
# ─────────────────────────────────────────────

def render_header(snap: SystemSnapshot) -> Panel:
    os_name  = f"{platform.system()} {platform.release()}"
    arch     = platform.machine()
    hostname = platform.node()

    t = Table.grid(padding=(0, 3))
    t.add_column(justify="left")
    t.add_column(justify="center")
    t.add_column(justify="right")

    left = Text.assemble(
        ("⬡ ", THEME["accent"]),
        ("SYSTEM PULSE", "bold bright_white"),
        ("  v1.0", THEME["dim"]),
    )
    center = Text.assemble(
        ("⏱ ", THEME["dim"]),
        (fmt_timestamp(snap.timestamp), THEME["accent"]),
    )
    right = Text.assemble(
        ("⬡ ", THEME["dim"]),
        (hostname, THEME["white"]),
        (f"  {os_name} [{arch}]", THEME["dim"]),
    )
    t.add_row(left, center, right)

    return Panel(t, style=THEME["bg"], border_style=THEME["accent"], padding=(0, 1))


# ─────────────────────────────────────────────
#  PANEL: CPU
# ─────────────────────────────────────────────

def render_cpu(cpu: CPUStats) -> Panel:
    grid = Table.grid(padding=(0, 1), expand=True)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    # ── Summary column ──
    summary = Table.grid(padding=(0, 0))
    summary.add_column()

    summary.add_row(Text(" TOTAL USAGE", style=THEME["label"]))
    summary.add_row(Text(
        f"  {cpu.total_percent:5.1f}%",
        style=f"bold {usage_color(cpu.total_percent)} {THEME['bg']}"
    ))
    summary.add_row(Text(""))

    bar_line = Text.assemble((" [", THEME["dim"]))
    bar_line.append_text(render_bar(cpu.total_percent, 22))
    bar_line.append("]", THEME["dim"])
    summary.add_row(bar_line)

    summary.add_row(Text(""))
    summary.add_row(Text(
        f"  {len(cpu.per_core_percent)} logical cores",
        style=THEME["dim"]
    ))

    # ── Per-core columns ──
    half = (len(cpu.per_core_percent) + 1) // 2

    def core_table_left(cores: list, offset: int = 0) -> Table:
        """id | bar | pct — for the left core column."""
        t = Table(box=None, show_header=False, padding=(0, 1), expand=True)
        t.add_column("id",  style=THEME["dim"],   width=5)
        t.add_column("bar", ratio=1)
        t.add_column("pct", width=8, justify="right")
        for i, pct in enumerate(cores):
            t.add_row(
                f"C{i + offset:02d}",
                render_bar(pct, 14),
                Text(f"{pct:5.1f}%", style=f"bold {usage_color(pct)}"),
            )
        return t

    def core_table_right(cores: list, offset: int = 0) -> Table:
        """id | bar | pct — for the right core column (same layout, mirrored feel)."""
        t = Table(box=None, show_header=False, padding=(0, 1), expand=True)
        t.add_column("id",  style=THEME["dim"],   width=5)
        t.add_column("bar", ratio=1)
        t.add_column("pct", width=8, justify="right")
        for i, pct in enumerate(cores):
            t.add_row(
                f"C{i + offset:02d}",
                render_bar(pct, 14),
                Text(f"{pct:5.1f}%", style=f"bold {usage_color(pct)}"),
            )
        return t

    grid.add_row(
        summary,
        core_table_left(cpu.per_core_percent[:half], 0),
        core_table_right(cpu.per_core_percent[half:], half),
    )

    return Panel(
        grid,
        title=f"[{THEME['header']}] CPU [/]",
        border_style=THEME["border"],
        box=box.ROUNDED,
        padding=(0, 1),
    )


# ─────────────────────────────────────────────
#  PANEL: MEMORY
# ─────────────────────────────────────────────

def render_memory(mem: MemoryStats) -> Panel:
    used_gb  = mem.used_bytes      / 1024**3
    total_gb = mem.total_bytes     / 1024**3
    avail_gb = mem.available_bytes / 1024**3

    t = Table.grid(padding=(0, 2), expand=True)
    t.add_column(ratio=1)
    t.add_column(ratio=2)

    # Stats column
    stats = Table(box=None, show_header=False, padding=(0, 1))
    stats.add_column(style=THEME["label"], width=10)
    stats.add_column(style=THEME["white"], justify="right")
    stats.add_row("TOTAL", f"{total_gb:.2f} GB")
    stats.add_row("USED",  Text(f"{used_gb:.2f} GB",  style=usage_color(mem.percent)))
    stats.add_row("FREE",  Text(f"{avail_gb:.2f} GB", style=THEME["normal"]))
    stats.add_row("USAGE", Text(f"{mem.percent:.1f}%", style=f"bold {usage_color(mem.percent)}"))

    # Visual bar column
    vis = Table.grid(padding=(0, 0))
    vis.add_column()
    vis.add_row(Text(""))
    vis.add_row(Text.assemble(
        ("[", THEME["dim"]),
        render_bar(mem.percent, 38),
        ("]", THEME["dim"]),
    ))
    vis.add_row(Text(
        f"  {used_gb:.2f} GB / {total_gb:.2f} GB  ({mem.percent:.1f}% used)",
        style=THEME["dim"],
    ))

    t.add_row(stats, vis)

    return Panel(
        t,
        title=f"[{THEME['header']}] MEMORY [/]",
        border_style=THEME["border"],
        box=box.ROUNDED,
        padding=(0, 1),
    )


# ─────────────────────────────────────────────
#  PANEL: FOOTER
# ─────────────────────────────────────────────

def render_footer() -> Text:
    t = Text(justify="center")
    t.append(" Ctrl+C ", f"bold black on {THEME['label']}")
    t.append(" Exit  ", THEME["dim"])
    return t


# ─────────────────────────────────────────────
#  LAYOUT ASSEMBLY
# ─────────────────────────────────────────────

def build_layout(snap: SystemSnapshot) -> Layout:
    """
    Assemble a full-screen Layout from a SystemSnapshot.
    Called once per refresh cycle by the runner.
    """
    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="cpu",    size=10),
        Layout(name="memory", size=8),
        Layout(name="footer", size=1),
    )

    layout["header"].update(render_header(snap))
    layout["cpu"].update(render_cpu(snap.cpu))
    layout["memory"].update(render_memory(snap.memory))
    layout["footer"].update(Align(render_footer(), align="center"))

    return layout
