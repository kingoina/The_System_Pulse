import time
from core.models import SystemSnapshot
from core.collector.cpu import collect_cpu
from core.collector.memory import collect_memory

def collect_system_snapshot() -> SystemSnapshot:
    return SystemSnapshot(
        timestamp=time.time(),
        cpu=collect_cpu(),
        memory=collect_memory()
    )

