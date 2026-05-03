import time
from core.collector.system import collect_system_snapshot
from core.logger.JSON_logger import log_snapshot

def run_monitor(interval:float=1.0):

    while True:
        snapshot = collect_system_snapshot()
        log_snapshot(snapshot)
        print(snapshot)
        time.sleep(interval)

