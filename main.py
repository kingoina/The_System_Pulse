from core.models import  CPUStats,MemoryStats,SystemSnapshot
import  time
cpu = CPUStats(35.5,[300.0,60.6])
mem = MemoryStats(4000000,45000000,45000000,56.45)
snapshot = SystemSnapshot(time.time(),cpu,mem)

print(snapshot)