import psutil
from core.models import MemoryStats

def collect_memory() -> MemoryStats:

    curr_memory = psutil.virtual_memory()
    return MemoryStats(
        total_bytes = curr_memory.total,
        used_bytes = curr_memory.used,
        available_bytes = curr_memory.available,
        percent = curr_memory.percent
    )

