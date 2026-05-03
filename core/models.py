from dataclasses import dataclass

@dataclass
class CPUStats:
    total_percent:float
    per_core_percent:list[float]

@dataclass
class MemoryStats:
    total_bytes:int
    used_bytes:int
    available_bytes:int
    percent:float

@dataclass
class SystemSnapshot:
    timestamp:float
    cpu:CPUStats
    memory:MemoryStats