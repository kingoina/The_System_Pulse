# System Pulse 🖥️

A professional terminal-based system monitoring dashboard built with Python and Rich.
Real-time CPU and memory monitoring with clean, structured panels designed for
developers and system administrators.

## Features

- **Real-time CPU monitoring** — total usage + per-core breakdown
- **Memory tracking** — used, free, total with visual progress bar
- **JSON logging** — every snapshot saved to `logs/system.jsonl`
- **Color-coded alerts** — green → yellow → red based on usage thresholds
- **1-second refresh** — accurate, flicker-free live updates
- **Cross-platform** — works on Windows, macOS, and Linux

---

## Project Structure

```
The_System_Pulse/
├── core/
│   ├── models.py              # Data structures (CPUStats, MemoryStats, SystemSnapshot)
│   ├── collector/
│   │   ├── cpu.py             # CPU data collection
│   │   ├── memory.py          # Memory data collection
│   │   └── system.py          # Orchestrates snapshot collection
│   ├── logger/
│   │   └── JSON_logger.py     # Logs snapshots to JSONL format
│   └── ui/
│       └── dashboard.py       # Rich terminal UI renderer
└── main.py                    # Entry point
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/kingoina/The_System_Pulse
cd The_System_Pulse
```

**2. Create a virtual environment**
```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install rich psutil
```

---

## Usage

```bash
python main.py
```

Press `Ctrl+C` to exit cleanly.

---

## Logs

Every snapshot is automatically saved to `logs/system.jsonl` in JSON Lines format:

```json
{"timestamp": 1746308847.23, "cpu": {"total_percent": 42.5, "per_core_percent": [55.1, 30.2]}, "memory": {...}, "timestamp_iso": "2026-05-03T22:07:27"}
```

---

## Color Thresholds

| Usage     | Color  |
|-----------|--------|
| < 50%     | 🟢 Green  |
| 50% – 75% | 🟡 Yellow |
| 75% – 90% | 🔴 Red    |
| > 90%     | 🔴 Bold Red (Critical) |

---

## Requirements

- Python 3.9+
- `rich`
- `psutil`

---

## Roadmap

- [ ] Disk usage panel
- [ ] Network speed panel (↑/↓ live rates)
- [ ] Top processes panel
- [ ] Alert thresholds config
- [ ] Export logs to CSV

---

## License

MIT
