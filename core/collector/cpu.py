import psutil
from core.models import CPUStats

def collect_cpu() -> CPUStats:

    total = psutil.cpu_percent(interval=0.5)
    per_core = psutil.cpu_percent(interval=None,percpu=True)

    return CPUStats(total_percent=total,per_core_percent=per_core)


