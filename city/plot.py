from dataclasses import dataclass, field
from typing import List


LAND_USE_RESIDENTIAL = "residential"
LAND_USE_COMMERCIAL  = "commercial"
LAND_USE_MIXED       = "mixed"
LAND_USE_EMPTY       = "empty"


@dataclass
class Plot:
    id: int
    x: int
    y: int
    land_use: str = LAND_USE_EMPTY
    value: float = 100.0
    accessibility: float = 0.0

    household_ids: List[int] = field(default_factory=list)
    firm_ids:      List[int] = field(default_factory=list)

    def is_occupied(self) -> bool:
        return bool(self.household_ids or self.firm_ids)

    def resident_count(self) -> int:
        return len(self.household_ids)

    def firm_count(self) -> int:
        return len(self.firm_ids)

    def __repr__(self):
        return (
            f"Plot(id={self.id}, pos=({self.x},{self.y}), "
            f"use={self.land_use}, value={self.value:.1f}, "
            f"hh={len(self.household_ids)}, firms={len(self.firm_ids)})"
        )